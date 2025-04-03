from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os, math, zlib, base64, logging, string
import aiohttp
from pydantic import BaseModel
from typing import Optional, List, Union

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)

class GenerateRequest(BaseModel):
    mode: str
    format: str = "dec"
    strict_validation: bool = True
    min_entropy: float = 7.0
    max_compression: float = 1.3
    # Параметры для режима limited:
    min: Optional[int] = 0
    max: Optional[int] = 100
    count: Optional[int] = 10
    # Параметры для режима infinite:
    bits: Optional[int] = 128
    # Параметры для режима password:
    password_length: Optional[int] = 12
    password_complexity: Optional[str] = "medium"  # допустимые значения: low, medium, high
    cipher_method: Optional[str] = "direct"  # допустимые значения: direct, rot13, reversed

def format_number(n: int, fmt: str) -> str:
    if fmt == "hex":
        return hex(n)[2:]
    if fmt == "bin":
        return bin(n)[2:]
    if fmt == "base64":
        if n == 0:
            return base64.b64encode(b'\x00').decode()
        return base64.b64encode(n.to_bytes((n.bit_length() + 7) // 8, 'big')).decode()
    return str(n)

async def get_qrng_bytes(length: int = 64) -> bytes:
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={length}&type=uint8"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                data = await response.json()
                return bytes(data["data"])
    except Exception as e:
        logging.error("Failed to get quantum random bytes: %s", e)
        return os.urandom(length)

class RandomValidator:
    def __init__(self, data: Union[List[int], bytes, str], expected_range: Optional[tuple] = None):
        if isinstance(data, str):
            self.byte_data = data.encode()
        elif isinstance(data, list):
            self.byte_data = str(data).encode()
        else:
            self.byte_data = data
        self.data = data
        self.expected_range = expected_range

    def compression_ratio(self) -> float:
        compressed = zlib.compress(self.byte_data)
        return len(compressed) / len(self.byte_data)

    def entropy(self) -> float:
        freq = {}
        for b in self.byte_data:
            freq[b] = freq.get(b, 0) + 1
        total = len(self.byte_data)
        return -sum((c / total) * math.log2(c / total) for c in freq.values())

    def chi_square_test(self):
        if isinstance(self.data, list) and self.expected_range is not None:
            expected_min, expected_max = self.expected_range
            range_size = expected_max - expected_min + 1
            n = len(self.data)
            expected_count = n / range_size
            counts = {}
            for num in self.data:
                counts[num] = counts.get(num, 0) + 1
            chi_square = 0
            for value in range(expected_min, expected_max + 1):
                observed = counts.get(value, 0)
                chi_square += (observed - expected_count) ** 2 / expected_count
            return chi_square, range_size - 1
        return None

    def summary(self) -> dict:
        summary = {
            "compression_ratio": round(self.compression_ratio(), 4),
            "entropy_bits_per_byte": round(self.entropy(), 4)
        }
        chi_test = self.chi_square_test()
        if chi_test is not None:
            chi_stat, dof = chi_test
            summary["chi_square_statistic"] = round(chi_stat, 4)
            summary["chi_square_degrees_of_freedom"] = dof
        return summary

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    try:
        with open("static/index.html", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error("Error loading HTML: %s", e)
        raise HTTPException(status_code=500, detail="Error loading page")

@app.post("/generate")
async def generate(req: GenerateRequest):
    mode = req.mode
    fmt = req.format
    strict = req.strict_validation
    min_entropy = req.min_entropy
    max_compression = req.max_compression

    if mode == "limited":
        min_val = req.min
        max_val = req.max
        count = max(1, min(req.count, 2048))
        byte_length_per_number = 4
        raw = await get_qrng_bytes(count * byte_length_per_number)
        values = [
            min_val + int.from_bytes(raw[i:i+byte_length_per_number], 'big') % (max_val - min_val + 1)
            for i in range(0, len(raw), byte_length_per_number)
        ]
        formatted = [format_number(v, fmt) for v in values]
        validator = RandomValidator(values, expected_range=(min_val, max_val))
        response = {
            "numbers": formatted
        }
    elif mode == "infinite":
        bits = req.bits
        byte_len = max(1, bits // 8)
        raw = await get_qrng_bytes(byte_len)
        value = int.from_bytes(raw, "big")
        formatted = format_number(value, fmt)
        validator = RandomValidator(raw)
        response = {
            "number": formatted
        }
    elif mode == "password":
        complexity = req.password_complexity.lower()
        if complexity == "low":
            charset = string.ascii_lowercase
        elif complexity == "medium":
            charset = string.ascii_letters + string.digits
        elif complexity == "high":
            charset = string.ascii_letters + string.digits + string.punctuation
        else:
            return JSONResponse({"error": "Invalid password complexity"}, status_code=400)

        password_length = req.password_length
        random_bytes = await get_qrng_bytes(password_length * 4)
        password_chars = []
        for i in range(0, len(random_bytes), 4):
            chunk = random_bytes[i:i+4]
            if len(chunk) < 4:
                break
            number = int.from_bytes(chunk, 'big')
            index = number % len(charset)
            password_chars.append(charset[index])
        password = "".join(password_chars)

        cipher_method = req.cipher_method.lower()
        if cipher_method == "rot13":
            import codecs
            password = codecs.encode(password, 'rot_13')
        elif cipher_method == "reversed":
            password = password[::-1]
        elif cipher_method != "direct":
            return JSONResponse({"error": "Invalid cipher method"}, status_code=400)

        validator = RandomValidator(random_bytes)
        response = {
            "password": password
        }
    else:
        return JSONResponse({"error": "Invalid mode"}, status_code=400)

    validation = validator.summary()
    if strict and (validation['entropy_bits_per_byte'] < min_entropy or validation['compression_ratio'] > max_compression):
        return JSONResponse({
            "error": "Generated data rejected — insufficient randomness.",
            "validation": validation
        }, status_code=406)

    response["validation"] = validation
    response["mode"] = mode
    response["format"] = fmt
    return response

@app.get("/api/generate")
async def api_generate(
    mode: str = "infinite",
    fmt: str = "dec",
    min: int = 0,
    max: int = 100,
    count: int = 256,
    bits: int = 128,
    strict_validation: bool = True,
    min_entropy: float = 7.0,
    max_compression: float = 1.3,
    password_length: int = 12,
    password_complexity: str = "medium",
    cipher_method: str = "direct"
):
    req = GenerateRequest(
        mode=mode,
        format=fmt,
        min=min,
        max=max,
        count=count,
        bits=bits,
        strict_validation=strict_validation,
        min_entropy=min_entropy,
        max_compression=max_compression,
        password_length=password_length,
        password_complexity=password_complexity,
        cipher_method=cipher_method
    )
    return await generate(req)