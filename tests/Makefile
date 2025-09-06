# Makefile для запуска тестов cupychecker

.PHONY: help install test test-helpers test-checker test-unit test-integration test-fast test-coverage clean

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Показать справку
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости для тестов
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	pip install -r requirements-test.txt

test: ## Запустить все тесты
	@echo "$(GREEN)Запуск всех тестов...$(NC)"
	python3 run_tests.py

test-helpers: ## Запустить тесты модуля helpers
	@echo "$(GREEN)Запуск тестов helpers...$(NC)"
	python3 run_tests.py helpers

test-checker: ## Запустить тесты модуля checker
	@echo "$(GREEN)Запуск тестов checker...$(NC)"
	python3 run_tests.py checker

test-unit: ## Запустить только unit тесты
	@echo "$(GREEN)Запуск unit тестов...$(NC)"
	python3 run_tests.py unit

test-integration: ## Запустить только интеграционные тесты
	@echo "$(GREEN)Запуск интеграционных тестов...$(NC)"
	python3 run_tests.py integration

test-fast: ## Запустить быстрые тесты (исключая медленные)
	@echo "$(GREEN)Запуск быстрых тестов...$(NC)"
	python3 run_tests.py fast

test-coverage: ## Запустить тесты с покрытием кода
	@echo "$(GREEN)Запуск тестов с покрытием...$(NC)"
	python3 run_tests.py coverage

test-watch: ## Запустить тесты в режиме наблюдения (требует pytest-watch)
	@echo "$(GREEN)Запуск тестов в режиме наблюдения...$(NC)"
	ptw --runner "python3 run_tests.py"

clean: ## Очистить временные файлы
	@echo "$(GREEN)Очистка временных файлов...$(NC)"
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint: ## Запустить линтеры
	@echo "$(GREEN)Запуск линтеров...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 ../cupychecker/cupychecker/ tests/; \
	else \
		echo "$(YELLOW)flake8 не установлен, пропускаем линтинг$(NC)"; \
	fi

format: ## Форматировать код
	@echo "$(GREEN)Форматирование кода...$(NC)"
	@if command -v black >/dev/null 2>&1; then \
		black ../cupychecker/cupychecker/ tests/; \
	else \
		echo "$(YELLOW)black не установлен, пропускаем форматирование$(NC)"; \
	fi

check: lint test ## Запустить линтинг и тесты

# Алиасы для быстрого доступа
t: test
th: test-helpers
tc: test-checker
tu: test-unit
ti: test-integration
tf: test-fast
tcov: test-coverage
