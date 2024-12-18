# Задание 4

## Условие

Разработать ассемблер и интерпретатор для учебной виртуальной машины
(УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к
которой задается из командной строки. Результатом работы ассемблера является
бинарный файл в виде последовательности байт, путь к которому задается из
командной строки. Дополнительный ключ командной строки задает путь к файлу-
логу, в котором хранятся ассемблированные инструкции в духе списков
“ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.

Форматом для файла-лога и файла-результата является **csv**.

Необходимо реализовать приведенные тесты для всех команд, а также
написать и отладить тестовую программу.

### Загрузка константы

| А        | B         |
|----------|-----------|
| Биты 0—5 | Биты 6—21 |
| 49       | Константа |

Размер команды: 3 байт. Операнд: поле B. Результат: регистр-аккумулятор.

    Тест (A=49, B=909):
    0x71, 0xE3, 0x00

### Чтение из памяти

| А        | B         |
|----------|-----------|
| Биты 0—5 | Биты 6—33 |
| 41       | Адрес     |

Размер команды: 5 байт. Операнд: значение в памяти по адресу, которым 
является поле B. Результат: регистр-аккумулятор.

    Тест (A=41, B=168):
    0x29, 0x2A, 0x00, 0x00, 0x00

### Запись в память

| A        | B         |
|----------|-----------|
| Биты 0—5 | Биты 6-33 |
| 23       | Адрес     |

Размер команды: 5 байт. Операнд: регистр-аккумулятор. Результат: значение 
в памяти по адресу, которым является поле B.

    Тест (A=23, B=394):
    0x97, 0x62, 0x00, 0x00, 0x00

### Унарная операция: унарный минус

| A        |
|----------|
| Биты 0—5 |
| 42       |

Размер команды: 1 байт. Операнд: значение в памяти по адресу, которым 
является регистр-аккумулятор. Результат: регистр-аккумулятор.

    Тест (A=42):
    0x2A

---

## Реализация языка

### Загрузка константы

**Синтаксис:**

```asm
LOAD #<значение>
```

**Описание:** Команда загружает константное значение в регистр-аккумулятор.

**Пример:**

```asm
LOAD #100
```

Запишет значение 100 в регистр-аккумулятор.

### Запись в память

**Синтаксис:**

```asm
WRITE [<адрес>]
```

**Описание:** Команда записывает данные из регистра-аккумулятора в ячейку памяти по адресу, которым является поле B.

**Пример:**

```asm
WRITE [100]
```

Запишет значение из регистра-аккумулятора в ячейку памяти по адресу [100].

### Загрузка из памяти

**Синтаксис:**

```asm
READ [<адрес>]
```

**Описание:** Загружает значение из ячейки памяти по адресу, которым является поле B, в регистр-аккумулятор.

**Пример:**

```asm
READ [100]
```

Запишет значение из ячейки памяти по адресу 100 в регистр-аккумулятор.

### Унарный минус

**Синтаксис:**

```asm
MINUS
```

**Описание:** Умножает на -1 значение, записанное в регистре-аккумуляторе, результат записывается в регистр-аккумулятор. 

---
# Установка и запуск

Для начала, убедитесь, что у вас установлен Python. Затем выполните следующие шаги:
1. Установка программы и переход в директорию
   ```bash
   git clone <URL репозитория>
   cd <директория проекта>
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```
3. Установите необходимые зависимости (pytest для тестов):
   ```bash
   pip install pytest
   ```
4. Запуск ассемблера:
    ```bash
   python assembler.py <source_file> <bin_file> <log_file>
    ```
   где 
   - **source_file** - файл с текстом исходной команды
   - **bin_file** - бинарный файл (результат работы ассемблера)
   - **log_file** - файл-лог
5. Запуск интерпретатора:
    ```bash
   python interpreter.py <bin_file> <result_file> <start> <end>
    ```
   где 
   - **bin_file** - бинарный файл
   - **result_file** - файл со значениями из диапазона памяти УВМ
   - **start** - начало диапазона памяти (включительно)
   - **end** - конец диапазона памяти (невключительно)

# Пример работы:
### Файл с текстом исходной команды:
```asm
LOAD #-100
WRITE [0]
LOAD #-200
WRITE [1]
LOAD #300
WRITE [2]
LOAD #400
WRITE [3]
READ [0]
MINUS
WRITE [0]
READ [1]
MINUS
WRITE [1]
READ [2]
MINUS
WRITE [2]
READ [3]
MINUS
WRITE [3]
```

### Файл-лог для ассемблированных инструкций:
```csv
LOAD	A=49	B=-100
WRITE	A=23	B=0
LOAD	A=49	B=-200
WRITE	A=23	B=1
LOAD	A=49	B=300
WRITE	A=23	B=2
LOAD	A=49	B=400
WRITE	A=23	B=3
READ	A=41	B=0
MINUS	A=42
WRITE	A=23	B=0
READ	A=41	B=1
MINUS	A=42
WRITE	A=23	B=1
READ	A=41	B=2
MINUS	A=42
WRITE	A=23	B=2
READ	A=41	B=3
MINUS	A=42
WRITE	A=23	B=3
```

### Файл-результат для ячеек памяти из диапазона от 0 до 4:
```csv
MEMORY[0]	100
MEMORY[1]	200
MEMORY[2]	-300
MEMORY[3]	-400
```
