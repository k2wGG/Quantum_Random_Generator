# 🎲 Quantum True Random Generator

![Quantum](https://img.shields.io/badge/random-quantum-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)

[en **English version**](README_EN.md)

Простой и удобный веб-интерфейс для генерации истинно случайных чисел с использованием **квантовой энтропии** от [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/). Проект поддерживает генерацию чисел в различных системах исчисления и обладает многоязычным интерфейсом.

---

## 🚀 Возможности

- **Два режима генерации**:
  - 🎯 Ограниченный диапазон (от мин. до макс.).
  - ♾️ Истинный бесконечный режим (генерация чисел с заданным количеством бит).
- **Выбор формата числа**:
  - Десятичный (`DEC`)
  - Шестнадцатеричный (`HEX`)
  - Двоичный (`BIN`)
  - Base64 (`Base64`)
- **Мультиязычный интерфейс**:
  - 🇷🇺 Русский
  - en Английский
- **Автоматическая проверка качества случайности** (энтропия и коэффициент сжатия).

---

## ⚙️ Как это работает?

### 🎯 Ограниченный диапазон:
- Пользователь задаёт диапазон и количество чисел.
- Генерация квантовых байтов и масштабирование в указанный диапазон.

### ♾️ Истинный бесконечный режим:
- Пользователь выбирает длину числа в битах.
- Получение байтов от квантового сервера и объединение их в число указанной длины.

---

## ⚙️ Проверка на истинную случайность

Каждое число проверяется по следующим критериям:

- **Коэффициент сжатия (Compression ratio)**  
  Чем ближе к `1.0`, тем выше случайность.

- **Энтропия (Entropy bits per byte)**  
  Чем ближе к `8.0`, тем выше истинность случайности.

---

## 🚀 Запуск проекта

### 📌 Требования

- Python 3.8+
- `pip` для установки пакетов

### 🛠️ Установка и запуск

Клонируй репозиторий:

```bash
git clone https://github.com/k2wGG/Quantum_Random_Generator.git
cd Quantum_Random_Generator
```

Установи зависимости:

```bash
pip install -r requirements.txt
```

Запусти сервер:

```bash
uvicorn main:app --reload
```

Открой приложение в браузере:

```
http://127.0.0.1:8000
```

---

## 🛠️ Технологии и ресурсы

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк для backend
- [ANU QRNG](https://qrng.anu.edu.au/) — источник квантовой энтропии
- [Uvicorn](https://www.uvicorn.org/) — сервер для FastAPI

---
