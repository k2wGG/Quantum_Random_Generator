# 🎲 Quantum True Random Generator

![Quantum](https://img.shields.io/badge/random-quantum-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)

[en English version](README_EN.md)

Простой и гибкий веб-интерфейс для генерации **истинно случайных чисел** на основе **квантовой энтропии** от [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/).

---

## 🚀 Возможности

- **Два режима генерации**:
  - 🎯 Ограниченный диапазон: числа от `min` до `max`, заданные пользователем.
  - ♾️ Бесконечный режим: генерация чисел с произвольным количеством бит (от 8 до 4096).

- **Поддержка форматов**:
  - 🔢 Decimal (`dec`)
  - 🔡 Hexadecimal (`hex`)
  - ⚙️ Binary (`bin`)
  - 🎲 Base64 (`base64`)

- **Настройка проверки качества случайности**:
  - 🔐 `Strict Validation` — отклоняет числа, если они не проходят порог энтропии и сжатия.
  - 📈 `Min Entropy` — минимум бит энтропии на байт (до 8.0).
  - 📉 `Max Compression Ratio` — максимум допустимого сжатия (близко к 1.0 — хорошо).

- **Интерфейс на двух языках**:
  - 🇷🇺 Русский
  - en English

- **Сохранение настроек** в `localStorage` браузера.
- 📊 Гистограмма распределения полученных чисел.
- 💾 Экспорт результатов в `.json`.

---

## 🧠 Как работает генерация?

### 🔬 Источник случайности
Мы используем [ANU Quantum Random Numbers Server](https://qrng.anu.edu.au/) — он получает данные из фотонных интерферометров, где результат наблюдения не может быть предсказан, что обеспечивает **истинную квантовую случайность**.

### 📐 Ограниченный диапазон (Limited Range)
1. Загружается необходимое количество байтов.
2. Числа масштабируются в диапазон от `min` до `max`.
3. Проверяются на:
   - энтропию (Shannon entropy)
   - коэффициент сжатия (zlib-compression ratio)

### ♾️ Бесконечный режим (Infinite mode)
1. Генерируется число заданной битовой длины (до 4096 бит).
2. Байты собираются в одно целое число.
3. Применяется форматирование (hex, bin и т.д.)
4. Проверка на энтропию и сжатие.

Формула масштабирования диапазона:
```python
range_size = max - min + 1
max_acceptable = (256 ** n_bytes // range_size) * range_size - 1

while True:
    value = get_random_value(n_bytes)
    if value <= max_acceptable:
        return min + (value % range_size)
```

---

## 📋 Проверка истинной случайности

Каждый блок данных проходит статистическую оценку:

- **Энтропия** (Shannon entropy):
  - 8.0 = идеальная случайность
  - 0.0 = полная предсказуемость

- **Коэффициент сжатия**:
  - Чем ближе к 1.0, тем хуже сжимаемость → выше случайность

Если `Strict Validation` включён — генерация повторяется до прохождения порогов.

---

## ⚙️ Установка и запуск

```bash
git clone https://github.com/k2wGG/Quantum_Random_Generator.git
cd Quantum_Random_Generator
pip install -r requirements.txt
uvicorn main:app --reload
```

Перейти в браузере: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Используемые технологии

- [FastAPI](https://fastapi.tiangolo.com/) — асинхронный Python-фреймворк
- [Uvicorn](https://www.uvicorn.org/) — сервер для FastAPI
- [Tailwind CSS](https://tailwindcss.com/) — для интерфейса
- [Chart.js](https://www.chartjs.org/) — визуализация распределения
- [ANU QRNG](https://qrng.anu.edu.au/) — квантовый генератор случайных чисел

---

Разработано с ❤️ для экспериментов, криптографии и энтропийных исследований.
