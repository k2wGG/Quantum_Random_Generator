# 🎲 Quantum True Random Generator

![Quantum](https://img.shields.io/badge/random-quantum-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)

[en English version](README_EN.md)

Это веб-приложение предоставляет гибкий интерфейс для генерации **истинно случайных чисел** с использованием квантовой энтропии, получаемой с [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/). Приложение реализует несколько режимов генерации и шифрования, включая демонстрационное постквантовое шифрование (PQ) на основе алгоритма Kyber и AES-GCM.

```mermaid
flowchart TD
    A["User Interface (Browser)"]
    B["Choose Mode"]
    C1["Limited Mode: Input Range (min, max, count)"]
    C2["Infinite Mode: Input Bit Length"]
    C3["Password Mode: Input Password Settings"]
    D1["Fetch Quantum Random Bytes (ANU API / os.urandom)"]
    D2["Fetch Quantum Random Bytes (ANU API / os.urandom)"]
    D3["Fetch Quantum Random Bytes (ANU API / os.urandom)"]
    E1["Generate Random Numbers"]
    E2["Generate Big Number"]
    E3["Generate Password"]
    F3["Optional Encryption (Direct, ROT13, Reversed, AES, PQ)"]
    G["Validate Randomness (Entropy, Compression Ratio, χ²-Test)"]
    H["Form JSON Response"]
    I["Display Result in Browser"]

    A --> B
    B -- "Limited" --> C1
    B -- "Infinite" --> C2
    B -- "Password" --> C3

    C1 --> D1
    C2 --> D2
    C3 --> D3

    D1 --> E1
    D2 --> E2
    D3 --> E3

    E1 --> G
    E2 --> G
    E3 --> F3
    F3 --> G

    G --> H
    H --> I

```

---

## 🚀 Возможности

- **Режимы генерации:**
  - **Limited Range:** Генерация чисел в заданном диапазоне (min–max).
  - **Infinite:** Генерация одного большого числа с указанной битовой длиной.
  - **Password:** Генерация случайного пароля с возможностью выбора сложности.

- **Форматы вывода:**  
  Поддерживаются Decimal, Hex, Binary и Base64.

- **Методы шифрования для пароля:**
  - **Direct:** Без шифрования.
  - **ROT13:** Простейшее симметричное преобразование.
  - **Reversed:** Реверс строки.
  - **AES:** Шифрование с использованием AES-CBC (PKCS7).
  - **PQ (Kyber + AES-GCM):** Постквантовое шифрование с использованием алгоритма Kyber (через [kyber-py](https://pypi.org/project/kyber-py/)) для инкапсуляции и AES-GCM для симметричного шифрования.

- **Квантовая энтропия:**  
  Для генерации случайных чисел используется API квантового генератора ANU. При недоступности API применяется `os.urandom`.

- **Валидация случайности:**  
  Выполняется расчет энтропии, коэффициента сжатия (через zlib) и χ²‑теста для оценки качества данных.

- **Современный веб-интерфейс:**  
  Реализовано на [FastAPI](https://fastapi.tiangolo.com/) с сервером [Uvicorn](https://uvicorn.org/), использован [Tailwind CSS](https://tailwindcss.com/) и [Chart.js](https://www.chartjs.org/) для визуализации.

---

## 🛠️ Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/your_username/Quantum_Random_Generator.git
   cd Quantum_Random_Generator
   ```

2. **Создайте и активируйте виртуальное окружение (рекомендуется Python 3.10 или 3.11):**

   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

   *requirements.txt*:
   ```txt
   fastapi
   uvicorn[standard]
   aiohttp
   kyber-py
   cryptography
   pydantic
   ```

4. **Запустите сервер:**

   ```bash
   uvicorn main:app --reload
   ```

5. **Откройте приложение в браузере:**  
   Перейдите по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📐 Как это работает

- **Генерация случайных чисел:**  
  Приложение запрашивает квантовые случайные байты с сервера ANU. Если API недоступен, используется `os.urandom`.

- **Режим "Password":**  
  Генерируется случайный пароль на основе выбранного набора символов (низкая, средняя или высокая сложность). После генерации пароль может быть зашифрован с использованием одного из методов:
  - **AES:** Шифрование с использованием AES-CBC.
  - **PQ (Kyber + AES-GCM):** Постквантовое шифрование, где алгоритм Kyber генерирует общий секрет, используемый для создания симметричного ключа (через SHA256), который применяется в AES-GCM.

- **Валидация:**  
  Расчет энтропии, коэффициента сжатия и теста χ² помогает оценить качество случайных данных.

---

## 🔒 Квантовые и постквантовые технологии

- **Квантовая энтропия:**  
  Используется для генерации истинно случайных чисел на основе квантовых процессов.

- **Постквантовое шифрование:**  
  Режим PQ демонстрирует гибридное шифрование, где Kyber (через kyber-py) используется для инкапсуляции ключа, а AES-GCM – для симметричного шифрования. Это направление помогает повысить устойчивость системы к квантовым атакам.

- **Возможные расширения:**  
  В будущем можно интегрировать квантовое распределение ключей (QKD) и другие квантово-устойчивые протоколы для обмена секретами.

---

## 📋 Дополнительные улучшения

- **Логирование:**  
  Приложение ведёт логирование ошибок, например, при недоступности квантового API.
  
- **Гибкая настройка:**  
  Пользователь может выбирать режим генерации, формат вывода, сложность пароля и метод шифрования через веб-интерфейс.

---

Разработано с ❤️ для экспериментов, исследований в области криптографии и квантовой случайности.
