#!/bin/bash
# Быстрые команды для тестирования cupychecker

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Быстрые команды для тестирования cupychecker${NC}"
echo "=================================================="

# Функция для показа справки
show_help() {
    echo -e "${YELLOW}Доступные команды:${NC}"
    echo "  ./quick_commands.sh help     - Показать эту справку"
    echo "  ./quick_commands.sh install  - Установить зависимости"
    echo "  ./quick_commands.sh test     - Запустить все тесты"
    echo "  ./quick_commands.sh helpers  - Тесты helpers"
    echo "  ./quick_commands.sh checker  - Тесты checker"
    echo "  ./quick_commands.sh fast     - Быстрые тесты"
    echo "  ./quick_commands.sh coverage - Тесты с покрытием"
    echo "  ./quick_commands.sh watch    - Тесты в режиме наблюдения"
    echo "  ./quick_commands.sh example  - Запустить примеры"
    echo "  ./quick_commands.sh clean    - Очистить временные файлы"
    echo ""
    echo -e "${YELLOW}Алиасы:${NC}"
    echo "  ./quick_commands.sh t        - test"
    echo "  ./quick_commands.sh h        - helpers"
    echo "  ./quick_commands.sh c        - checker"
    echo "  ./quick_commands.sh f        - fast"
    echo "  ./quick_commands.sh cov      - coverage"
}

# Функция для установки зависимостей
install_deps() {
    echo -e "${GREEN}📦 Установка зависимостей...${NC}"
    pip install -r requirements-test.txt
    echo -e "${GREEN}✅ Зависимости установлены!${NC}"
}

# Функция для запуска тестов
run_tests() {
    local test_type=${1:-"all"}
    echo -e "${GREEN}🧪 Запуск тестов: ${test_type}${NC}"
    python3 run_tests.py "$test_type"
}

# Функция для запуска примеров
run_examples() {
    echo -e "${GREEN}📚 Запуск примеров...${NC}"
    python3 example_usage.py
}

# Функция для очистки
clean_files() {
    echo -e "${GREEN}🧹 Очистка временных файлов...${NC}"
    rm -rf __pycache__/
    rm -rf .pytest_cache/
    rm -rf htmlcov/
    rm -rf .coverage
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${GREEN}✅ Очистка завершена!${NC}"
}

# Функция для режима наблюдения
watch_tests() {
    echo -e "${GREEN}👀 Запуск тестов в режиме наблюдения...${NC}"
    if command -v ptw >/dev/null 2>&1; then
        ptw --runner "python run_tests.py"
    else
        echo -e "${RED}❌ pytest-watch не установлен. Установите: pip install pytest-watch${NC}"
        echo -e "${YELLOW}Альтернатива: используйте 'make test-watch'${NC}"
    fi
}

# Основная логика
case "${1:-help}" in
    "help"|"-h"|"--help")
        show_help
        ;;
    "install"|"i")
        install_deps
        ;;
    "test"|"t")
        run_tests "all"
        ;;
    "helpers")
        run_tests "helpers"
        ;;
    "checker"|"c")
        run_tests "checker"
        ;;
    "fast"|"f")
        run_tests "fast"
        ;;
    "coverage"|"cov")
        run_tests "coverage"
        ;;
    "watch"|"w")
        watch_tests
        ;;
    "example"|"e")
        run_examples
        ;;
    "clean"|"cl")
        clean_files
        ;;
    "h")
        # Алиас для helpers
        run_tests "helpers"
        ;;
    *)
        echo -e "${RED}❌ Неизвестная команда: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
