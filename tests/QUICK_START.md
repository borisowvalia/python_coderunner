# 🚀 Быстрый старт с тестами cupychecker

## Установка

```bash
# Установить зависимости
pip3 install -r requirements-test.txt

# Или через make
make install
```

## Быстрый запуск тестов

### 1. Через скрипт run_tests.py

```bash
# Все тесты
python3 run_tests.py

# Только тесты helpers
python3 run_tests.py helpers

# Только тесты checker  
python3 run_tests.py checker

# Тесты с покрытием
python3 run_tests.py coverage
```

### 2. Через быстрые команды (quick_commands.sh)

```bash
# Показать справку
./quick_commands.sh help

# Все тесты
./quick_commands.sh test

# Тесты helpers (алиас: h)
./quick_commands.sh h

# Тесты checker (алиас: c)
./quick_commands.sh c

# Быстрые тесты (алиас: f)
./quick_commands.sh f

# С покрытием (алиас: cov)
./quick_commands.sh cov

# Примеры использования
./quick_commands.sh example
```

### 3. Через Makefile

```bash
# Показать справку
make help

# Все тесты
make test

# Тесты helpers (алиас: th)
make th

# Тесты checker (алиас: tc)
make tc

# Быстрые тесты (алиас: tf)
make tf

# С покрытием (алиас: tcov)
make tcov
```

### 4. Прямо через pytest

```bash
# Все тесты
pytest

# Конкретный файл
pytest test_helpers.py

# Конкретный тест
pytest test_helpers.py::TestTestHelperVar::test_var_simple_assignment -v

# С покрытием
pytest --cov=../cupychecker/cupychecker --cov-report=html
```

## Примеры использования в процессе разработки

### 1. Быстрая проверка после изменений

```bash
# После изменения helpers.py
./quick_commands.sh h

# После изменения checker.py  
./quick_commands.sh c

# Быстрая проверка всех тестов
./quick_commands.sh f
```

### 2. Отладка конкретного теста

```bash
# Запуск с подробным выводом
pytest test_helpers.py::TestTestHelperVar::test_var_simple_assignment -v -s

# Запуск с отладчиком
pytest test_helpers.py::TestTestHelperVar::test_var_simple_assignment --pdb
```

### 3. Проверка покрытия кода

```bash
# Создать HTML отчет
python3 run_tests.py coverage

# Открыть отчет
open htmlcov/index.html
```

## Структура тестов

```
tests/
├── test_helpers.py      # Тесты для модуля helpers (35 тестов)
├── test_checker.py      # Тесты для модуля checker (17 тестов)
├── conftest.py          # Конфигурация pytest и фикстуры
├── pytest.ini          # Настройки pytest
├── requirements-test.txt # Зависимости для тестов
├── run_tests.py         # Скрипт для запуска тестов
├── quick_commands.sh    # Быстрые команды
├── Makefile            # Makefile с командами
├── example_usage.py    # Примеры использования
└── README.md           # Подробная документация
```

## Что тестируется

### Модуль helpers (TestHelper)

- **var()** - проверка переменных (10 тестов)
- **call()** - проверка вызовов функций (10 тестов)  
- **output()** - проверка вывода (7 тестов)
- **contains()** - проверка содержания кода (6 тестов)
- **Интеграционные тесты** (2 теста)

### Модуль checker

- **run_code()** - выполнение кода (3 теста)
- **check_result()** - проверка результатов (14 тестов)

## Полезные команды

```bash
# Очистить временные файлы
make clean

# Запустить только unit тесты
make test-unit

# Запустить только интеграционные тесты
make test-integration

# Запустить тесты в режиме наблюдения
make test-watch

# Проверить линтинг
make lint

# Форматировать код
make format
```

## Интеграция с IDE

### VS Code
1. Установите расширение Python
2. Настройте pytest в settings.json:
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests"]
}
```

### PyCharm
1. Откройте настройки проекта
2. Перейдите в Python Integrated Tools
3. Выберите pytest как Default test runner
4. Укажите путь к тестам: `tests`

## Непрерывная интеграция

Пример для GitHub Actions:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r tests/requirements-test.txt
        pip install -e .
    - name: Run tests
      run: |
        cd tests
        python3 run_tests.py
```

## Решение проблем

### Ошибка "python: command not found"
Используйте `python3` вместо `python`:
```bash
python3 run_tests.py
```

### Ошибка "pytest не найден"
Установите зависимости:
```bash
pip3 install -r requirements-test.txt
```

### Тесты не находят модуль cupychecker
Убедитесь, что вы находитесь в директории tests:
```bash
cd tests
python3 run_tests.py
```

## Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте этот файл
2. Посмотрите подробную документацию в README.md
3. Запустите примеры: `./quick_commands.sh example`
