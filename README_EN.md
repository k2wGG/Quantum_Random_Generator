# 🎲 Quantum True Random Generator

![Quantum](https://img.shields.io/badge/random-quantum-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)

[🇷🇺 Русская версия](README.md)

A simple yet powerful web interface for generating **true random numbers** based on **quantum entropy** from the [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/).

---

## 🚀 Features

- **Two generation modes**:
  - 🎯 Limited Range: generate numbers within a custom range.
  - ♾️ Infinite Mode: generate a single number with up to 4096 bits.

- **Number formats**:
  - 🔢 Decimal (`dec`)
  - 🔡 Hexadecimal (`hex`)
  - ⚙️ Binary (`bin`)
  - 🎲 Base64 (`base64`)

- **Randomness validation**:
  - 🔐 `Strict Validation` — reject values that don't meet quality criteria.
  - 📈 `Min Entropy` — lower bound for bits per byte.
  - 📉 `Max Compression Ratio` — upper limit for compressibility.

- **Multilingual interface**:
  - en English
  - 🇷🇺 Russian

- **Settings persistence** via browser `localStorage`
- 📊 Histogram chart for generated value distribution
- 💾 Export results as `.json`

---

## 🧠 How does it work?

### 🔬 Quantum randomness source
We use [ANU QRNG](https://qrng.anu.edu.au/), which utilizes photonic quantum processes (beam-splitting interference) to ensure **non-deterministic outcomes** — true randomness guaranteed by quantum mechanics.

### 📐 Limited Range mode
1. Bytes are fetched from the quantum server.
2. Scaled into range using:
```python
result = min + (random_value % (max - min + 1))
```
3. Each result is evaluated for entropy and compressibility.

### ♾️ Infinite Mode
1. Fetches enough bytes to match bit length (e.g., 1024 bits = 128 bytes).
2. Concatenates into one large number.
3. Formats the output (e.g., hex, base64).
4. Validates for entropy and compression ratio.

---

## 🧪 Randomness Quality Checks

Each generated value is analyzed via:

- **Entropy (Shannon entropy per byte)**:
  - 8.0 = perfect randomness
  - 0.0 = no randomness

- **Compression Ratio** (zlib):
  - Close to 1.0 = highly random
  - Higher values = more predictable structure

With `Strict Validation` enabled, data is rejected and retried if metrics are not met.

---

## ⚙️ Installation & Run

```bash
git clone https://github.com/k2wGG/Quantum_Random_Generator.git
cd Quantum_Random_Generator
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Technologies

- [FastAPI](https://fastapi.tiangolo.com/) — modern Python web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server for FastAPI
- [Tailwind CSS](https://tailwindcss.com/) — UI styling
- [Chart.js](https://www.chartjs.org/) — graph visualization
- [ANU QRNG](https://qrng.anu.edu.au/) — quantum random number source

---

Created with ❤️ for cryptography, experimentation, and data entropy research.
