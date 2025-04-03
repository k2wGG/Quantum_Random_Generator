# 🎲 Quantum True Random Generator

![Quantum](https://img.shields.io/badge/random-quantum-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)

A simple and flexible web interface for generating **truly random numbers** based on **quantum entropy** provided by the [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/). This project includes advanced randomness validation, asynchronous requests, and statistical quality evaluation.

---

## 🚀 Features

- **Two Generation Modes**:
  - 🎯 **Limited Range:** Generate numbers within a user-defined range (`min` to `max`).
  - ♾️ **Infinite Mode:** Generate a single large number with a customizable bit length (from 8 up to 4096 bits).

- **Output Formats Supported**:
  - 🔢 Decimal (`dec`)
  - 🔡 Hexadecimal (`hex`)
  - ⚙️ Binary (`bin`)
  - 🎲 Base64 (`base64`)

- **Advanced Randomness Validation**:
  - 🔐 **Strict Validation:** Rejects data if entropy or compression ratio thresholds are not met.
  - 📈 **Min Entropy:** Minimum Shannon entropy per byte (up to 8.0, where 8.0 indicates perfect randomness).
  - 📉 **Max Compression Ratio:** Maximum allowed compression ratio (closer to 1.0 is better).
  - 📊 **χ² Test:** Statistical test to verify the uniform distribution of generated numbers.
  - 📈 **Frequency Distribution:** Calculation and return of a frequency table for visual analysis of value uniqueness and distribution.

- **Asynchronous Requests**:
  - Uses [aiohttp](https://docs.aiohttp.org/) for non-blocking retrieval of quantum random bytes.

- **Bilingual Interface**:
  - 🇺🇸 English
  - [Русский](README.md)

- **Settings Persistence**:
  - Saves user preferences in the browser’s `localStorage`.

- 📊 **Histogram Visualization**:
  - Displays the frequency distribution of generated numbers using [Chart.js](https://www.chartjs.org/).

- 💾 **Export Results:**
  - Allows exporting the generated results as a `.json` file.

---

## 🧠 How Does It Work?

### 🔬 Quantum Source of Randomness
The project utilizes the [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/) which obtains data from photon interferometers. This process ensures **true quantum randomness**.

### 📐 Limited Range Mode
1. **Asynchronous Request:** The required number of bytes is fetched asynchronously using aiohttp.
2. **Scaling:** The bytes are converted to numbers and scaled to fit within the range defined by `min` and `max`.
3. **Validation:**
   - Calculates **Shannon Entropy** to assess randomness.
   - Determines the **Compression Ratio** (via zlib) — less compressible data indicates higher randomness.
   - Performs a **χ² Test** to verify the uniformity of the distribution.
4. **Distribution Analysis:** Computes a frequency table for visual inspection of the value distribution.

### ♾️ Infinite Mode
1. **Number Generation:** Asynchronously retrieves bytes to construct a single large number of a specified bit length (up to 4096 bits).
2. **Formatting:** The number is formatted into the selected output format (dec, hex, bin, base64).
3. **Validation:** Checks the number for sufficient entropy and an acceptable compression ratio.

A sample scaling algorithm:
```python
range_size = max - min + 1
max_acceptable = (256 ** n_bytes // range_size) * range_size - 1

while True:
    value = get_random_value(n_bytes)
    if value <= max_acceptable:
        return min + (value % range_size)
```

---

## 📋 Randomness Quality Assurance

Each block of generated data undergoes comprehensive validation:

- **Entropy (Shannon Entropy):**
  - 8.0 bits/byte indicates perfect randomness.
  - Values below the threshold may signal insufficient randomness.

- **Compression Ratio:**
  - Ratios close to 1.0 indicate high randomness, as the data is less compressible.

- **χ² Test:**
  - Conducted to assess the uniformity of the generated numbers’ distribution.
  - The test results (χ² statistic and degrees of freedom) are included in the report.

If **Strict Validation** is enabled, generation is repeated until all thresholds are met.

---

## ⚙️ Installation and Running

```bash
git clone https://github.com/your_username/Quantum_Random_Generator.git
cd Quantum_Random_Generator
pip install -r requirements.txt
uvicorn main:app --reload
```

Open your browser at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) — Asynchronous Python web framework.
- [Uvicorn](https://www.uvicorn.org/) — ASGI server for FastAPI.
- [aiohttp](https://docs.aiohttp.org/) — Asynchronous HTTP client.
- [Tailwind CSS](https://tailwindcss.com/) — For styling the web interface.
- [Chart.js](https://www.chartjs.org/) — For visualizing the frequency distribution.
- [ANU QRNG](https://qrng.anu.edu.au/) — Quantum random number generator.
- [Pydantic](https://pydantic-docs.helpmanual.io/) — For data validation and type annotations.

---

Developed with ❤️ for experiments, cryptography, and entropy research.
