# Тесты для библиотеки cupychecker

Этот каталог содержит тесты для библиотеки cupychecker, которые можно быстро запускать в процессе разработки.

## Структура тестов

```
tests/
├── test_helpers.py      # Тесты для модуля helpers
├── test_checker.py      # Тесты для модуля checker
├── conftest.py          # Конфигурация pytest и фикстуры
├── pytest.ini          # Настройки pytest
├── requirements-test.txt # Зависимости для тестов
├── run_tests.py         # Скрипт для быстрого запуска тестов
└── README.md            # Этот файл
```

## Установка зависимостей

```bash
pip install -r requirements-test.txt
```

## Быстрый запуск тестов

### Использование скрипта run_tests.py

```bash
# Все тесты
python run_tests.py

# Только тесты модуля helpers
python run_tests.py helpers

# Только тесты модуля checker
python run_tests.py checker

# Только unit тесты
python run_tests.py unit

# Только интеграционные тесты
python run_tests.py integration

# Быстрые тесты (исключая медленные)
python run_tests.py fast

# Тесты с покрытием кода
python run_tests.py coverage
```

### Прямой запуск через pytest

```bash
# Все тесты
pytest

# Конкретный файл
pytest test_helpers.py

# Конкретный тест
pytest test_helpers.py::TestTestHelperVar::test_var_simple_assignment

# С подробным выводом
pytest -v

# Только unit тесты
pytest -m unit

# Исключая медленные тесты
pytest -m "not slow"
```

## Описание тестов

### test_helpers.py

Тесты для класса `TestHelper` и его методов:

- **TestTestHelperVar**: Тесты метода `var()` для проверки переменных
- **TestTestHelperCall**: Тесты метода `call()` для проверки вызовов функций
- **TestTestHelperOutput**: Тесты метода `output()` для проверки вывода
- **TestTestHelperContains**: Тесты метода `contains()` для проверки содержания кода
- **TestTestHelperIntegration**: Интеграционные тесты

### test_checker.py

Тесты для модуля `checker`:

- **TestRunCode**: Тесты функции `run_code()` для выполнения кода
- **TestCheckResult**: Тесты функции `check_result()` для проверки результатов

## Маркеры тестов

- `@pytest.mark.unit` - unit тесты
- `@pytest.mark.integration` - интеграционные тесты
- `@pytest.mark.slow` - медленные тесты

## Фикстуры

В `conftest.py` определены следующие фикстуры:

- `sample_code` - пример простого кода
- `sample_stdout` - пример простого вывода
- `complex_code` - пример комплексного кода
- `complex_stdout` - пример комплексного вывода

## Покрытие кода

Для создания отчета о покрытии кода:

```bash
python run_tests.py coverage
```

Отчет будет создан в `htmlcov/index.html`.

## Примеры использования

### Тестирование в процессе разработки

```bash
# Быстрая проверка после изменений в helpers
python run_tests.py helpers

# Проверка конкретного метода
pytest test_helpers.py::TestTestHelperVar::test_var_simple_assignment -v

# Проверка с покрытием только измененного кода
pytest test_helpers.py --cov=../cupychecker/cupychecker/helpers --cov-report=term-missing
```

### Отладка тестов

```bash
# Запуск с подробным выводом и остановкой на первой ошибке
pytest -xvs

# Запуск с отладочной информацией
pytest --pdb

# Запуск только упавших тестов
pytest --lf
```

## Интеграция с IDE

### VS Code

1. Установите расширение Python
2. Настройте pytest как тестовый фреймворк в settings.json:
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

Для настройки CI/CD можно использовать следующий пример для GitHub Actions:

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
        python run_tests.py
```
