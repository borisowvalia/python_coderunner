#!/usr/bin/env python3
"""
Скрипт для быстрого запуска тестов cupychecker
"""
import subprocess
import sys
import os
from pathlib import Path

def run_tests(test_type="all", verbose=True):
    """
    Запуск тестов
    
    Args:
        test_type (str): Тип тестов для запуска
            - "all": все тесты
            - "helpers": только тесты helpers
            - "checker": только тесты checker
            - "unit": только unit тесты
            - "integration": только интеграционные тесты
        verbose (bool): Подробный вывод
    """
    
    # Переходим в директорию с тестами
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    # Базовые аргументы pytest
    cmd = ["python3", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    # Выбираем тесты в зависимости от типа
    if test_type == "helpers":
        cmd.append("test_helpers.py")
    elif test_type == "checker":
        cmd.append("test_checker.py")
    elif test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    else:  # all
        cmd.append(".")
    
    print(f"Запуск тестов: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Все тесты прошли успешно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Тесты завершились с ошибкой (код: {e.returncode})")
        return False
    except FileNotFoundError:
        print("❌ pytest не найден. Установите зависимости:")
        print("pip install -r requirements-test.txt")
        return False

def run_coverage():
    """Запуск тестов с покрытием кода"""
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    cmd = [
        "python3", "-m", "pytest", 
        "--cov=../cupychecker/cupychecker",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v"
    ]
    
    print("Запуск тестов с покрытием кода...")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Отчет о покрытии создан в htmlcov/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка при создании отчета о покрытии (код: {e.returncode})")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        test_type = "all"  # По умолчанию запускаем все тесты
    else:
        test_type = sys.argv[1].lower()
    
    if test_type == "help" or test_type == "-h" or test_type == "--help":
        print("Использование:")
        print("  python run_tests.py [тип_тестов]")
        print("\nТипы тестов:")
        print("  all         - все тесты (по умолчанию)")
        print("  helpers     - только тесты модуля helpers")
        print("  checker     - только тесты модуля checker")
        print("  unit        - только unit тесты")
        print("  integration - только интеграционные тесты")
        print("  fast        - быстрые тесты (исключая медленные)")
        print("  coverage    - тесты с покрытием кода")
        print("\nПримеры:")
        print("  python run_tests.py")
        print("  python run_tests.py helpers")
        print("  python run_tests.py coverage")
        return
    
    if test_type == "coverage":
        success = run_coverage()
    else:
        success = run_tests(test_type)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
