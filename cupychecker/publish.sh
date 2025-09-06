#!/bin/bash
# Скрипт для быстрой публикации пакета cupychecker

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для показа справки
show_help() {
    echo -e "${GREEN}🚀 Скрипт публикации пакета cupychecker${NC}"
    echo "=================================================="
    echo -e "${YELLOW}Использование:${NC}"
    echo "  ./publish.sh [команда] [опции]"
    echo ""
    echo -e "${YELLOW}Команды:${NC}"
    echo "  help              - Показать эту справку"
    echo "  setup             - Настроить окружение для разработки"
    echo "  test              - Запустить тесты"
    echo "  build             - Собрать пакет"
    echo "  clean             - Очистить предыдущие сборки"
    echo "  check             - Проверить пакет"
    echo "  publish           - Публиковать patch версию"
    echo "  publish-patch     - Публиковать patch версию (0.1.0 -> 0.1.1)"
    echo "  publish-minor     - Публиковать minor версию (0.1.0 -> 0.2.0)"
    echo "  publish-major     - Публиковать major версию (0.1.0 -> 1.0.0)"
    echo "  publish-test      - Публиковать на TestPyPI"
    echo "  publish-version   - Публиковать конкретную версию"
    echo "  dev               - Быстрая разработка (тест + сборка)"
    echo ""
    echo -e "${YELLOW}Примеры:${NC}"
    echo "  ./publish.sh publish"
    echo "  ./publish.sh publish-minor"
    echo "  ./publish.sh publish-test"
    echo "  ./publish.sh publish-version 1.2.3"
    echo "  ./publish.sh dev"
    echo ""
    echo -e "${YELLOW}Алиасы:${NC}"
    echo "  p                 - publish"
    echo "  pt                - publish-test"
    echo "  pp                - publish-patch"
    echo "  pm                - publish-minor"
    echo "  pmj               - publish-major"
    echo "  pv                - publish-version"
    echo "  t                 - test"
    echo "  b                 - build"
    echo "  c                 - clean"
}

# Функция для настройки окружения
setup_env() {
    echo -e "${GREEN}🔧 Настройка окружения для разработки...${NC}"
    pip3 install --upgrade setuptools wheel build twine
    pip3 install -e .
    pip3 install -r ../tests/requirements-test.txt
    echo -e "${GREEN}✅ Окружение настроено!${NC}"
}

# Функция для запуска тестов
run_tests() {
    echo -e "${GREEN}🧪 Запуск тестов...${NC}"
    cd ../tests && python3 run_tests.py
}

# Функция для сборки пакета
build_package() {
    echo -e "${GREEN}🔨 Сборка пакета...${NC}"
    python3 publish.py --build-only
}

# Функция для очистки
clean_build() {
    echo -e "${GREEN}🧹 Очистка предыдущих сборок...${NC}"
    python3 publish.py --clean-only
}

# Функция для проверки пакета
check_package() {
    echo -e "${GREEN}🔍 Проверка пакета...${NC}"
    python3 -m twine check dist/*
}

# Функция для публикации
publish_package() {
    local version_type=${1:-"patch"}
    local test_only=${2:-false}
    local version=${3:-""}
    
    echo -e "${GREEN}🚀 Публикация пакета...${NC}"
    
    if [ -n "$version" ]; then
        python3 publish.py --version "$version"
    elif [ "$test_only" = true ]; then
        python3 publish.py --test-only
    else
        python3 publish.py --version-type "$version_type"
    fi
}

# Функция для быстрой разработки
dev_workflow() {
    echo -e "${GREEN}⚡ Быстрая разработка...${NC}"
    run_tests
    build_package
    check_package
    echo -e "${GREEN}✅ Готово! Пакет собран и проверен.${NC}"
}

# Функция для показа текущей версии
show_version() {
    echo -e "${GREEN}📦 Текущая версия:${NC}"
    python3 -c "import re; content=open('setup.cfg').read(); print(re.search(r'version\s*=\s*([^\s\n]+)', content).group(1))"
}

# Функция для показа файлов в dist
show_files() {
    echo -e "${GREEN}📁 Файлы в dist/:${NC}"
    if [ -d "dist" ]; then
        ls -la dist/
    else
        echo "Директория dist/ не существует"
    fi
}

# Основная логика
case "${1:-help}" in
    "help"|"-h"|"--help")
        show_help
        ;;
    "setup")
        setup_env
        ;;
    "test"|"t")
        run_tests
        ;;
    "build"|"b")
        build_package
        ;;
    "clean"|"c")
        clean_build
        ;;
    "check")
        check_package
        ;;
    "publish"|"p")
        publish_package "patch" false
        ;;
    "publish-patch"|"pp")
        publish_package "patch" false
        ;;
    "publish-minor"|"pm")
        publish_package "minor" false
        ;;
    "publish-major"|"pmj")
        publish_package "major" false
        ;;
    "publish-test"|"pt")
        publish_package "patch" true
        ;;
    "publish-version"|"pv")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Укажите версию: ./publish.sh publish-version 1.2.3${NC}"
            exit 1
        fi
        publish_package "patch" false "$2"
        ;;
    "dev")
        dev_workflow
        ;;
    "version")
        show_version
        ;;
    "files")
        show_files
        ;;
    *)
        echo -e "${RED}❌ Неизвестная команда: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
