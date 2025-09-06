# Makefile для управления пакетом cupychecker

.PHONY: help install test build clean publish publish-test publish-patch publish-minor publish-major

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Показать справку
	@echo "$(GREEN)Доступные команды для cupychecker:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить пакет в режиме разработки
	@echo "$(GREEN)Установка пакета в режиме разработки...$(NC)"
	pip3 install -e .

install-dev: ## Установить пакет с зависимостями для разработки
	@echo "$(GREEN)Установка пакета с зависимостями для разработки...$(NC)"
	pip3 install -e .
	pip3 install -r ../tests/requirements-test.txt

test: ## Запустить тесты
	@echo "$(GREEN)Запуск тестов...$(NC)"
	cd ../tests && python3 run_tests.py

test-helpers: ## Запустить тесты helpers
	@echo "$(GREEN)Запуск тестов helpers...$(NC)"
	cd ../tests && python3 run_tests.py helpers

test-checker: ## Запустить тесты checker
	@echo "$(GREEN)Запуск тестов checker...$(NC)"
	cd ../tests && python3 run_tests.py checker

build: ## Собрать пакет
	@echo "$(GREEN)Сборка пакета...$(NC)"
	python3 publish.py --build-only

clean: ## Очистить предыдущие сборки
	@echo "$(GREEN)Очистка предыдущих сборок...$(NC)"
	python3 publish.py --clean-only

check: ## Проверить пакет
	@echo "$(GREEN)Проверка пакета...$(NC)"
	python3 -m twine check dist/*

# Команды публикации
publish: ## Публиковать новую версию (patch)
	@echo "$(GREEN)Публикация новой версии (patch)...$(NC)"
	python3 publish.py

publish-patch: ## Публиковать patch версию (0.1.0 -> 0.1.1)
	@echo "$(GREEN)Публикация patch версии...$(NC)"
	python3 publish.py --version-type patch

publish-minor: ## Публиковать minor версию (0.1.0 -> 0.2.0)
	@echo "$(GREEN)Публикация minor версии...$(NC)"
	python3 publish.py --version-type minor

publish-major: ## Публиковать major версию (0.1.0 -> 1.0.0)
	@echo "$(GREEN)Публикация major версии...$(NC)"
	python3 publish.py --version-type major

publish-test: ## Публиковать на TestPyPI
	@echo "$(GREEN)Публикация на TestPyPI...$(NC)"
	python3 publish.py --test-only

publish-version: ## Публиковать конкретную версию (использование: make publish-version VERSION=1.2.3)
	@echo "$(GREEN)Публикация версии $(VERSION)...$(NC)"
	python3 publish.py --version $(VERSION)

# Команды для быстрой разработки
dev-setup: ## Настроить окружение для разработки
	@echo "$(GREEN)Настройка окружения для разработки...$(NC)"
	pip3 install --upgrade setuptools wheel build twine
	pip3 install -e .
	pip3 install -r ../tests/requirements-test.txt
	@echo "$(GREEN)✅ Окружение настроено!$(NC)"

dev-test: ## Быстрый тест во время разработки
	@echo "$(GREEN)Быстрый тест...$(NC)"
	cd ../tests && python3 run_tests.py fast

dev-build: ## Быстрая сборка для проверки
	@echo "$(GREEN)Быстрая сборка...$(NC)"
	python3 publish.py --build-only

# Команды для отладки
show-version: ## Показать текущую версию
	@echo "$(GREEN)Текущая версия:$(NC)"
	@python3 -c "import re; content=open('setup.cfg').read(); print(re.search(r'version\s*=\s*([^\s\n]+)', content).group(1))"

show-files: ## Показать файлы в dist/
	@echo "$(GREEN)Файлы в dist/:$(NC)"
	@ls -la dist/ 2>/dev/null || echo "Директория dist/ не существует"

# Алиасы для быстрого доступа
p: publish
pt: publish-test
pp: publish-patch
pm: publish-minor
pmj: publish-major
pv: publish-version
t: test
th: test-helpers
tc: test-checker
b: build
c: clean
