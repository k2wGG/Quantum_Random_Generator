from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os, math, zlib, requests, base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class RandomValidator:
    def __init__(self, numbers):
        self.byte_data = str(numbers).encode()

    def compression_ratio(self):
        return len(zlib.compress(self.byte_data)) / len(self.byte_data)

    def entropy(self):
        freq = {}
        for b in self.byte_data:
            freq[b] = freq.get(b, 0) + 1
        total = len(self.byte_data)
        return -sum((c / total) * math.log2(c / total) for c in freq.values())

    def summary(self):
        return {
            "compression_ratio": round(self.compression_ratio(), 4),
            "entropy_bits_per_byte": round(self.entropy(), 4)
        }

def get_qrng_bytes(length=64):
    try:
        r = requests.get(f"https://qrng.anu.edu.au/API/jsonI.php?length={length}&type=uint8", timeout=5)
        r.raise_for_status()
        return bytes(r.json()["data"])
    except:
        return os.urandom(length)

def format_number(n: int, fmt: str):
    if fmt == "hex": return hex(n)[2:]
    if fmt == "bin": return bin(n)[2:]
    if fmt == "base64": return base64.b64encode(n.to_bytes((n.bit_length()+7)//8, 'big')).decode()
    return str(n)

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    mode = data.get("mode")
    fmt = data.get("format", "dec")
    strict = data.get("strict_validation", True)
    min_entropy = float(data.get("min_entropy", 7.0))
    max_compression = float(data.get("max_compression", 1.3))

    if mode == "limited":
        min_val = int(data.get("min", 0))
        max_val = int(data.get("max", 100))
        count = min(max(int(data.get("count", 10)), 1), 2048)

        byte_length_per_number = 4
        raw = get_qrng_bytes(count * byte_length_per_number)

        values = [
            min_val + int.from_bytes(raw[i:i+byte_length_per_number], 'big') % (max_val - min_val + 1)
            for i in range(0, len(raw), byte_length_per_number)
        ]

        formatted = [format_number(v, fmt) for v in values]
        validator = RandomValidator(values)

    elif mode == "infinite":
        bits = int(data.get("bits", 128))
        byte_len = max(1, bits // 8)
        raw = get_qrng_bytes(byte_len)
        value = int.from_bytes(raw, "big")
        formatted = format_number(value, fmt)
        validator = RandomValidator(raw)
    else:
        return JSONResponse({"error": "Invalid mode"}, status_code=400)

    validation = validator.summary()
    if strict and (validation['entropy_bits_per_byte'] < min_entropy or validation['compression_ratio'] > max_compression):
        return JSONResponse({
            "error": "Generated data rejected — not random enough.",
            "validation": validation
        }, status_code=406)

    return {
        "numbers": formatted if isinstance(formatted, list) else None,
        "number": formatted if isinstance(formatted, str) else None,
        "validation": validation
    }

@app.get("/api/generate")
async def api_generate(mode: str = "infinite", fmt: str = "dec", min: int = 0, max: int = 100, count: int = 256, bits: int = 128, strict_validation: bool = True, min_entropy: float = 7.0, max_compression: float = 1.3):
    req = {
        "mode": mode, "format": fmt, "min": min, "max": max, "count": count, "bits": bits,
        "strict_validation": strict_validation, "min_entropy": min_entropy, "max_compression": max_compression
    }
    return await generate(Request(scope={"type": "http"}, receive=None, send=None, json=req))
