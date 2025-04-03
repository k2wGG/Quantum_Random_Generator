# 🎲 Quantum True Random Generator

![Quantum](https://img.shields.io/badge/random-quantum-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)

[🇷🇺 **Russian version**](README.md)

This project provides a simple and convenient web interface for generating truly random numbers using quantum entropy from [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/).

---

## 🔍 How it works

The project operates in two main modes:

### 🎯 Limited Range Mode

- User specifies:
  - minimum value;
  - maximum value;
  - number of random numbers.
- The application retrieves quantum random bytes from ANU Quantum API.
- Bytes are scaled to the specified range and returned to the user.

### ♾️ True Infinite Mode

- User selects the desired bit length for the random number using a slider.
- The application retrieves the required number of bytes from the quantum server.
- Bytes are combined into a single large number of arbitrary length (up to extremely large values).
- The resulting number is returned to the user along with randomness analysis.

---

## ⚙️ True Randomness Validation

Each generated number undergoes the following checks:

- **Compression Ratio**  
  The closer to `1.0`, the higher the randomness quality.

- **Entropy (bits per byte)**  
  The closer to `8.0`, the closer to true randomness.

---

## 🚀 How to Run the Project

### 📌 Requirements

- Python 3.8+
- `pip` for package installation

### 🛠️ Installation and Startup

Clone the repository:

```bash
git clone https://github.com/k2wGG/Quantum_Random_Generator.git
cd Quantum_Random_Generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

Open your web browser and navigate to:

```
http://127.0.0.1:8000
```

---

## 🛠️ Technologies and Resources

- [FastAPI](https://fastapi.tiangolo.com/) — backend framework
- [ANU QRNG](https://qrng.anu.edu.au/) — quantum entropy source
- [Uvicorn](https://www.uvicorn.org/) — FastAPI server

---
