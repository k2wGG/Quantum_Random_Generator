from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import requests, os, math, zlib, random, base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class TrueRandomValidator:
    def __init__(self, byte_data):
        self.byte_data = byte_data

    def compression_test(self):
        compressed = zlib.compress(self.byte_data)
        return len(compressed) / len(self.byte_data)

    def entropy_estimate(self):
        byte_counts = {}
        for b in self.byte_data:
            byte_counts[b] = byte_counts.get(b, 0) + 1
        entropy = -sum((count / len(self.byte_data)) * math.log2(count / len(self.byte_data)) 
                        for count in byte_counts.values())
        return entropy

    def summary(self):
        return {
            "compression_ratio": round(self.compression_test(), 4),
            "entropy_bits_per_byte": round(self.entropy_estimate(), 4),
        }

def get_quantum_random_bytes(length=64):
    try:
        response = requests.get(f'https://qrng.anu.edu.au/API/jsonI.php?length={length}&type=uint8', timeout=5)
        response.raise_for_status()
        return bytes(response.json()['data'])
    except:
        return os.urandom(length)

def format_number(number: int, fmt: str):
    if fmt == 'hex':
        return hex(number)[2:]
    elif fmt == 'bin':
        return bin(number)[2:]
    elif fmt == 'base64':
        byte_length = (number.bit_length() + 7) // 8
        return base64.b64encode(number.to_bytes(byte_length, 'big')).decode()
    else:
        return str(number)

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    mode = data.get('mode')
    fmt = data.get('format', 'dec')

    if mode == 'limited':
        min_val, max_val, count = int(data['min']), int(data['max']), min(int(data['count']), 1024)
        raw_bytes = get_quantum_random_bytes(count)
        numbers = [int(min_val + (b / 255) * (max_val - min_val)) for b in raw_bytes]
        formatted_numbers = [format_number(num, fmt) for num in numbers]
        result = {"numbers": formatted_numbers}

    elif mode == 'infinite':
        bits = int(data.get('bits', 128))
        byte_length = max(1, bits // 8)
        raw_bytes = get_quantum_random_bytes(byte_length)
        number = int.from_bytes(raw_bytes, 'big')
        formatted_number = format_number(number, fmt)
        result = {"number": formatted_number}
    else:
        return JSONResponse({"error": "Invalid mode"}, status_code=400)

    validator = TrueRandomValidator(raw_bytes)
    result["validation"] = validator.summary()
    return result
