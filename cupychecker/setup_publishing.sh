#!/bin/bash
# Скрипт для настройки окружения публикации пакета cupychecker

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Настройка окружения для публикации cupychecker${NC}"
echo "=================================================="

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 не найден. Установите Python 3.7+${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 найден: $(python3 --version)${NC}"

# Устанавливаем зависимости
echo -e "${YELLOW}📦 Устанавливаю зависимости...${NC}"
pip3 install --upgrade setuptools wheel build twine

# Устанавливаем пакет в режиме разработки
echo -e "${YELLOW}📦 Устанавливаю пакет в режиме разработки...${NC}"
pip3 install -e .

# Устанавливаем зависимости для тестов
echo -e "${YELLOW}📦 Устанавливаю зависимости для тестов...${NC}"
pip3 install -r ../tests/requirements-test.txt

# Создаем .pypirc если его нет
if [ ! -f ".pypirc" ]; then
    echo -e "${YELLOW}📝 Создаю .pypirc из примера...${NC}"
    cp .pypirc.example .pypirc
    echo -e "${YELLOW}⚠️  Отредактируйте .pypirc и вставьте ваши API токены${NC}"
else
    echo -e "${GREEN}✅ .pypirc уже существует${NC}"
fi

# Проверяем git
if command -v git &> /dev/null; then
    echo -e "${GREEN}✅ Git найден: $(git --version)${NC}"
else
    echo -e "${YELLOW}⚠️  Git не найден. Рекомендуется установить для создания тегов${NC}"
fi

# Запускаем тесты
echo -e "${YELLOW}🧪 Запускаю тесты...${NC}"
cd ../tests
if python3 run_tests.py; then
    echo -e "${GREEN}✅ Тесты прошли успешно!${NC}"
else
    echo -e "${RED}❌ Тесты не прошли. Исправьте ошибки перед публикацией${NC}"
    exit 1
fi

cd ../cupychecker

# Показываем текущую версию
echo -e "${YELLOW}📦 Текущая версия:${NC}"
python3 -c "import re; content=open('setup.cfg').read(); print(re.search(r'version\s*=\s*([^\s\n]+)', content).group(1))"

echo ""
echo -e "${GREEN}🎉 Настройка завершена!${NC}"
echo ""
echo -e "${YELLOW}Следующие шаги:${NC}"
echo "1. Отредактируйте .pypirc и вставьте ваши API токены"
echo "2. Протестируйте публикацию на TestPyPI:"
echo "   ./publish.sh publish-test"
echo "3. Публикуйте на PyPI:"
echo "   ./publish.sh publish"
echo ""
echo -e "${YELLOW}Полезные команды:${NC}"
echo "  ./publish.sh help     - Показать справку"
echo "  ./publish.sh test     - Запустить тесты"
echo "  ./publish.sh build    - Собрать пакет"
echo "  make help             - Показать команды make"
echo ""
echo -e "${BLUE}Документация: PUBLISH.md${NC}"
