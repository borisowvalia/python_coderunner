# 🚀 Публикация пакета cupychecker

Этот документ описывает, как публиковать новую версию пакета cupychecker в PyPI.

## 📋 Предварительные требования

1. **Установленные инструменты:**
   ```bash
   pip3 install --upgrade setuptools wheel build twine
   ```

2. **API токены PyPI:**
   - Получите токен на [PyPI](https://pypi.org/manage/account/token/)
   - Получите токен на [TestPyPI](https://test.pypi.org/manage/account/token/)

3. **Настройка .pypirc:**
   ```bash
   # Скопируйте .pypirc.example в .pypirc
   cp .pypirc.example .pypirc
   
   # Отредактируйте .pypirc и вставьте ваши токены
   nano .pypirc
   ```

## 🛠 Способы публикации

### 1. Через Python скрипт (рекомендуется)

```bash
# Публикация patch версии (0.1.0 -> 0.1.1)
python3 publish.py

# Публикация minor версии (0.1.0 -> 0.2.0)
python3 publish.py --version-type minor

# Публикация major версии (0.1.0 -> 1.0.0)
python3 publish.py --version-type major

# Публикация конкретной версии
python3 publish.py --version 1.2.3

# Публикация на TestPyPI
python3 publish.py --test-only

# Пропустить тесты
python3 publish.py --skip-tests

# Только сборка (без публикации)
python3 publish.py --build-only
```

### 2. Через bash скрипт

```bash
# Показать справку
./publish.sh help

# Публикация patch версии
./publish.sh publish

# Публикация minor версии
./publish.sh publish-minor

# Публикация major версии
./publish.sh publish-major

# Публикация на TestPyPI
./publish.sh publish-test

# Публикация конкретной версии
./publish.sh publish-version 1.2.3

# Быстрая разработка (тест + сборка)
./publish.sh dev
```

### 3. Через Makefile

```bash
# Показать справку
make help

# Публикация patch версии
make publish

# Публикация minor версии
make publish-minor

# Публикация major версии
make publish-major

# Публикация на TestPyPI
make publish-test

# Публикация конкретной версии
make publish-version VERSION=1.2.3

# Только сборка
make build

# Только тесты
make test
```

## 📦 Процесс публикации

Скрипт `publish.py` выполняет следующие шаги:

1. **Обновление версии** - автоматически увеличивает версию в `setup.cfg`
2. **Запуск тестов** - проверяет, что все тесты проходят
3. **Очистка** - удаляет предыдущие сборки
4. **Сборка пакета** - создает wheel и source distribution
5. **Проверка пакета** - проверяет пакет с помощью twine
6. **Создание git тега** - создает тег для новой версии
7. **Публикация** - загружает пакет в PyPI или TestPyPI

## 🔧 Настройка окружения

### Первоначальная настройка

```bash
# 1. Установите зависимости
make install-dev

# 2. Настройте .pypirc
cp .pypirc.example .pypirc
# Отредактируйте .pypirc и вставьте ваши токены

# 3. Проверьте настройку
python3 -m twine check dist/*
```

### Настройка для разработки

```bash
# Быстрая настройка
./publish.sh setup

# Или через make
make dev-setup
```

## 🧪 Тестирование перед публикацией

### Рекомендуемый workflow

1. **Сначала TestPyPI:**
   ```bash
   ./publish.sh publish-test
   ```

2. **Установите с TestPyPI:**
   ```bash
   pip3 install --index-url https://test.pypi.org/simple/ cupychecker
   ```

3. **Протестируйте:**
   ```bash
   python3 -c "import cupychecker; print('OK')"
   ```

4. **Публикуйте на PyPI:**
   ```bash
   ./publish.sh publish
   ```

## 📝 Управление версиями

### Семантическое версионирование

- **MAJOR** (1.0.0) - несовместимые изменения API
- **MINOR** (0.1.0) - новая функциональность с обратной совместимостью
- **PATCH** (0.0.1) - исправления ошибок с обратной совместимостью

### Примеры

```bash
# Текущая версия: 0.1.0

# Patch версия (исправления)
python3 publish.py --version-type patch
# Результат: 0.1.1

# Minor версия (новая функциональность)
python3 publish.py --version-type minor
# Результат: 0.2.0

# Major версия (breaking changes)
python3 publish.py --version-type major
# Результат: 1.0.0
```

## 🔍 Проверка пакета

### Локальная проверка

```bash
# Собрать пакет
python3 publish.py --build-only

# Проверить пакет
python3 -m twine check dist/*

# Установить локально
pip3 install dist/cupychecker-*.whl
```

### Проверка на TestPyPI

```bash
# Публиковать на TestPyPI
python3 publish.py --test-only

# Установить с TestPyPI
pip3 install --index-url https://test.pypi.org/simple/ cupychecker

# Проверить работу
python3 -c "from cupychecker.helpers import TestHelper; print('OK')"
```

## 🚨 Решение проблем

### Ошибка "Invalid credentials"

```bash
# Проверьте .pypirc
cat .pypirc

# Убедитесь, что токены правильные
python3 -m twine check dist/*
```

### Ошибка "Package already exists"

```bash
# Увеличьте версию
python3 publish.py --version-type patch

# Или укажите конкретную версию
python3 publish.py --version 1.2.3
```

### Ошибка "Tests failed"

```bash
# Запустите тесты отдельно
cd ../tests && python3 run_tests.py

# Исправьте ошибки и повторите
python3 publish.py
```

### Ошибка "Git tag already exists"

```bash
# Удалите тег
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# Или пропустите создание тега
python3 publish.py --skip-git
```

## 📚 Полезные команды

### Информация о пакете

```bash
# Показать текущую версию
python3 -c "import re; content=open('setup.cfg').read(); print(re.search(r'version\s*=\s*([^\s\n]+)', content).group(1))"

# Показать файлы в dist
ls -la dist/

# Показать информацию о пакете
python3 -m twine check dist/*
```

### Отладка

```bash
# Подробный вывод
python3 publish.py --version-type patch -v

# Только сборка
python3 publish.py --build-only

# Пропустить тесты
python3 publish.py --skip-tests
```

## 🔗 Полезные ссылки

- [PyPI](https://pypi.org/project/cupychecker/)
- [TestPyPI](https://test.pypi.org/project/cupychecker/)
- [Twine документация](https://twine.readthedocs.io/)
- [Python Packaging User Guide](https://packaging.python.org/)

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте этот документ
2. Запустите тесты: `make test`
3. Проверьте настройки: `python3 -m twine check dist/*`
4. Создайте issue в репозитории
