from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os, math, zlib, base64, logging
import aiohttp
from pydantic import BaseModel
from typing import Optional, List, Union

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)


class GenerateRequest(BaseModel):
    mode: str
    format: str = "dec"
    strict_validation: bool = True
    min_entropy: float = 7.0
    max_compression: float = 1.3
    min: Optional[int] = 0
    max: Optional[int] = 100
    count: Optional[int] = 10
    bits: Optional[int] = 128


def format_number(n: int, fmt: str) -> str:
    """
    Форматирует число в указанный формат (десятичный, шестнадцатеричный, двоичный, base64).
    """
    if fmt == "hex":
        return hex(n)[2:]
    if fmt == "bin":
        return bin(n)[2:]
    if fmt == "base64":
        # Обрабатываем случай n == 0 отдельно
        if n == 0:
            return base64.b64encode(b'\x00').decode()
        return base64.b64encode(n.to_bytes((n.bit_length() + 7) // 8, 'big')).decode()
    return str(n)


async def get_qrng_bytes(length: int = 64) -> bytes:
    """
    Асинхронно получает квантовые случайные байты через API qrng.anu.edu.au.
    В случае ошибки возвращает os.urandom.
    """
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={length}&type=uint8"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                data = await response.json()
                return bytes(data["data"])
    except Exception as e:
        logging.error("Не удалось получить квантовые случайные байты: %s", e)
        return os.urandom(length)


class RandomValidator:
    def __init__(self, data: Union[List[int], bytes], expected_range: Optional[tuple] = None):
        """
        data: либо список чисел (для режима 'limited'), либо байты (режим 'infinite').
        expected_range: кортеж (min, max) для режима 'limited' — используется для проведения χ²‑теста.
        """
        self.data = data
        # Для расчёта энтропии и коэффициента сжатия используем байтовое представление
        if isinstance(data, list):
            self.byte_data = str(data).encode()
        else:
            self.byte_data = data
        self.expected_range = expected_range

    def compression_ratio(self) -> float:
        """
        Вычисляет отношение размера сжатых данных к исходному размеру.
        """
        compressed = zlib.compress(self.byte_data)
        return len(compressed) / len(self.byte_data)

    def entropy(self) -> float:
        """
        Вычисляет энтропию по распределению байт в данных.
        """
        freq = {}
        for b in self.byte_data:
            freq[b] = freq.get(b, 0) + 1
        total = len(self.byte_data)
        return -sum((c / total) * math.log2(c / total) for c in freq.values())

    def chi_square_test(self):
        """
        Проводит χ²‑тест для проверки равномерности распределения, если data — список чисел
        и задан expected_range. Возвращает кортеж (χ²‑статистика, число степеней свободы)
        или None, если тест не применим.
        """
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
        """
        Возвращает сводку по валидации данных, включая коэффициент сжатия,
        энтропию и (если применимо) результаты χ²‑теста.
        """
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
        logging.error("Ошибка при загрузке HTML: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка загрузки страницы")


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
        # Генерируем список чисел в диапазоне [min_val, max_val]
        values = [
            min_val + int.from_bytes(raw[i:i + byte_length_per_number], 'big') % (max_val - min_val + 1)
            for i in range(0, len(raw), byte_length_per_number)
        ]
        formatted = [format_number(v, fmt) for v in values]
        validator = RandomValidator(values, expected_range=(min_val, max_val))
        # Вычисляем таблицу частот для визуализации распределения
        frequency = {}
        for v in values:
            frequency[v] = frequency.get(v, 0) + 1
        frequency_distribution = sorted(frequency.items())
    elif mode == "infinite":
        bits = req.bits
        byte_len = max(1, bits // 8)
        raw = await get_qrng_bytes(byte_len)
        value = int.from_bytes(raw, "big")
        formatted = format_number(value, fmt)
        validator = RandomValidator(raw)
        frequency_distribution = None
    else:
        return JSONResponse({"error": "Неверный режим генерации"}, status_code=400)

    validation = validator.summary()
    # Строгая проверка случайности: отклоняем результат, если энтропия или коэффициент сжатия не удовлетворяют порогам
    if strict and (validation['entropy_bits_per_byte'] < min_entropy or validation['compression_ratio'] > max_compression):
        return JSONResponse({
            "error": "Сгенерированные данные отклонены — недостаточная случайность.",
            "validation": validation
        }, status_code=406)

    response = {
        "validation": validation,
        "format": fmt,
        "mode": mode
    }
    if mode == "limited":
        response["numbers"] = formatted
        response["frequency_distribution"] = frequency_distribution
    elif mode == "infinite":
        response["number"] = formatted

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
    max_compression: float = 1.3
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
        max_compression=max_compression
    )
    return await generate(req)