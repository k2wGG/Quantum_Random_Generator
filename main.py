from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import math
import zlib
import random

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

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    mode = data.get('mode')

    if mode == 'limited':
        min_val = int(data['min'])
        max_val = int(data['max'])
        count = min(int(data['count']), 1024)
        raw_bytes = get_quantum_random_bytes(count)
        numbers = [int(min_val + (b / 255) * (max_val - min_val)) for b in raw_bytes]
        result = {"numbers": numbers}

    elif mode == 'infinite':
        bits = int(data.get('bits', 128))
        byte_length = max(1, bits // 8)
        raw_bytes = get_quantum_random_bytes(byte_length)
        number = int.from_bytes(raw_bytes, 'big')
        result = {"number": str(number)}

    else:
        return JSONResponse({"error": "Invalid mode"}, status_code=400)

    validator = TrueRandomValidator(raw_bytes)
    result["validation"] = validator.summary()

    return result
