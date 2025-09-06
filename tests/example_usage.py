#!/usr/bin/env python3
"""
Пример использования тестов cupychecker в процессе разработки
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cupychecker'))

from cupychecker.helpers import TestHelper


def example_development_workflow():
    """Пример рабочего процесса разработки с тестами"""
    
    print("🔧 Пример рабочего процесса разработки с тестами")
    print("=" * 60)
    
    # 1. Разработчик пишет код
    student_code = """
x = 10
y = "hello"
print(f"x = {x}, y = {y}")
"""
    
    print("1. Код студента:")
    print(student_code)
    
    # 2. Создаем TestHelper для проверки
    helper = TestHelper(student_code, "x = 10, y = hello")
    
    # 3. Проверяем переменные
    print("\n2. Проверка переменных:")
    var_x_result = helper.var("x", 10)
    var_y_result = helper.var("y", "hello")
    
    print(f"   x = 10: {var_x_result}")
    print(f"   y = 'hello': {var_y_result}")
    
    # 4. Проверяем вызов функции
    print("\n3. Проверка вызова функции:")
    call_result = helper.call("print")
    print(f"   print() вызван: {call_result}")
    
    # 5. Проверяем вывод
    print("\n4. Проверка вывода:")
    output_result = helper.output("x = 10, y = hello")
    print(f"   Вывод корректен: {output_result}")
    
    # 6. Проверяем содержание кода
    print("\n5. Проверка содержания кода:")
    contains_result = helper.contains("f\"x = {x}")
    print(f"   Содержит f-строку: {contains_result}")
    
    # 7. Общий результат
    all_checks = [var_x_result, var_y_result, call_result, output_result, contains_result]
    all_passed = all(check is True for check in all_checks)
    
    print(f"\n6. Общий результат: {'✅ ВСЕ ПРОВЕРКИ ПРОШЛИ' if all_passed else '❌ ЕСТЬ ОШИБКИ'}")
    
    return all_passed


def example_error_handling():
    """Пример обработки ошибок"""
    
    print("\n\n🚨 Пример обработки ошибок")
    print("=" * 60)
    
    # Код с ошибками
    problematic_code = """
x = 5  # Должно быть 10
y = "world"  # Должно быть "hello"
print(x)  # Должен быть print(y)
"""
    
    print("1. Проблемный код:")
    print(problematic_code)
    
    helper = TestHelper(problematic_code, "5")
    
    # Проверяем и показываем ошибки
    print("\n2. Анализ ошибок:")
    
    var_x_result = helper.var("x", 10)
    if var_x_result is not True:
        print(f"   ❌ Переменная x: {var_x_result}")
    
    var_y_result = helper.var("y", "hello")
    if var_y_result is not True:
        print(f"   ❌ Переменная y: {var_y_result}")
    
    call_result = helper.call("print", ["y"])
    if call_result is not True:
        print(f"   ❌ Вызов print(y): {call_result}")
    
    output_result = helper.output("hello")
    if output_result is not True:
        print(f"   ❌ Вывод 'hello': {output_result}")


def example_quick_test():
    """Пример быстрого тестирования во время разработки"""
    
    print("\n\n⚡ Пример быстрого тестирования")
    print("=" * 60)
    
    # Быстрая проверка нового кода
    new_code = "result = 2 + 3 * 4"
    helper = TestHelper(new_code, "")
    
    # Проверяем только то, что нужно
    result = helper.var("result", 14)  # 2 + 3 * 4 = 14
    print(f"Код: {new_code}")
    print(f"Результат: {result}")
    
    if result is True:
        print("✅ Код корректен!")
    else:
        print(f"❌ Ошибка: {result}")


if __name__ == "__main__":
    print("🧪 Примеры использования тестов cupychecker")
    print("=" * 60)
    
    # Запускаем примеры
    example_development_workflow()
    example_error_handling()
    example_quick_test()
    
    print("\n\n📚 Для запуска полных тестов используйте:")
    print("   python run_tests.py")
    print("   make test")
    print("   pytest")
