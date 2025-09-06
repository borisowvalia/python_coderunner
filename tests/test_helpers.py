"""
Тесты для модуля helpers библиотеки cupychecker
"""
import pytest
import ast
from cupychecker.helpers import TestHelper


class TestTestHelperVar:
    """Тесты для метода var() класса TestHelper"""
    
    def test_var_simple_assignment(self):
        """Тест простого присваивания переменной"""
        helper = TestHelper("x = 10", "")
        result = helper.var("x", 10)
        assert result is True
    
    def test_var_string_assignment(self):
        """Тест присваивания строки"""
        helper = TestHelper("name = 'John'", "")
        result = helper.var("name", "John")
        assert result is True
    
    def test_var_list_assignment(self):
        """Тест присваивания списка"""
        helper = TestHelper("items = [1, 2, 3]", "")
        result = helper.var("items", [1, 2, 3])
        assert result is True
    
    def test_var_multiple_assignments_last_value(self):
        """Тест множественных присваиваний - проверяет последнее значение"""
        helper = TestHelper("x = 1\nx = 2", "")
        result = helper.var("x", 2)
        assert result is True
    
    def test_var_multiple_assignments_wrong_value(self):
        """Тест множественных присваиваний - неправильное значение"""
        helper = TestHelper("x = 1\nx = 2", "")
        result = helper.var("x", 1)
        assert isinstance(result, str)
        assert "было переписвоено значение 2" in result
    
    def test_var_undeclared_variable(self):
        """Тест необъявленной переменной"""
        helper = TestHelper("y = 5", "")
        result = helper.var("x", 5)
        assert isinstance(result, str)
        assert "не объявлена" in result
    
    def test_var_string_with_spaces(self):
        """Тест строки с пробелами - пробелы должны игнорироваться"""
        helper = TestHelper("text = 'hello world'", "")
        result = helper.var("text", "helloworld")
        assert result is True
    
    def test_var_complex_expression(self):
        """Тест сложного выражения"""
        helper = TestHelper("result = 2 + 3 * 4", "")
        # Для сложных выражений используется ast.unparse
        result = helper.var("result", "2+3*4")
        assert result is True
    
    def test_var_syntax_error(self):
        """Тест синтаксической ошибки в коде"""
        helper = TestHelper("x = ", "")
        result = helper.var("x", 5)
        assert isinstance(result, SyntaxError)
    
    def test_var_custom_message(self):
        """Тест с пользовательским сообщением об ошибке"""
        helper = TestHelper("x = 1", "")
        result = helper.var("x", 2, msg="Ошибка в переменной x")
        assert result == "Ошибка в переменной x"


class TestTestHelperCall:
    """Тесты для метода call() класса TestHelper"""
    
    def test_call_simple_function(self):
        """Тест простого вызова функции"""
        helper = TestHelper("print('hello')", "")
        result = helper.call("print")
        assert result is True
    
    def test_call_function_with_args(self):
        """Тест вызова функции с аргументами"""
        helper = TestHelper("print(123, sep='\\t')", "")
        # Метод call использует issubset, поэтому проверяем только часть аргументов
        result = helper.call("print", [123])
        assert result is True
    
    def test_call_function_with_exact_args(self):
        """Тест вызова функции с точными аргументами"""
        helper = TestHelper("print(123, sep='\\t')", "")
        # Проверяем все аргументы (\\t интерпретируется как \t)
        result = helper.call("print", [123, ("sep", "\t")])
        assert result is True
    
    def test_call_function_wrong_args(self):
        """Тест вызова функции с неправильными аргументами"""
        helper = TestHelper("print(123)", "")
        result = helper.call("print", [123, ("sep", "\\t")])
        assert isinstance(result, str)
        assert "не соответствует" in result
    
    def test_call_function_not_found(self):
        """Тест несуществующего вызова функции"""
        helper = TestHelper("x = 1", "")
        result = helper.call("print")
        assert isinstance(result, str)
        assert "Не найден вызов функции" in result
    
    def test_call_method_call(self):
        """Тест вызова метода объекта"""
        helper = TestHelper("df.head()", "")
        result = helper.call("head")
        assert result is True
    
    def test_call_nested_method(self):
        """Тест вложенного вызова метода"""
        helper = TestHelper("df.groupby('col').sum()", "")
        result = helper.call("sum")
        assert result is True
    
    def test_call_with_variable_args(self):
        """Тест вызова с переменными в аргументах"""
        helper = TestHelper("print(123, end=var)", "")
        result = helper.call("print", [("end", "var")])
        assert result is True
    
    def test_call_syntax_error(self):
        """Тест синтаксической ошибки в коде"""
        helper = TestHelper("print(", "")
        result = helper.call("print")
        assert isinstance(result, SyntaxError)
    
    def test_call_custom_message(self):
        """Тест с пользовательским сообщением об ошибке"""
        helper = TestHelper("x = 1", "")
        result = helper.call("print", msg="Функция print не найдена")
        assert result == "Функция print не найдена"


class TestTestHelperOutput:
    """Тесты для метода output() класса TestHelper"""
    
    def test_output_exact_match(self):
        """Тест точного совпадения вывода"""
        helper = TestHelper("", "hello\nworld")
        result = helper.output("hello\nworld")
        assert result is True
    
    def test_output_with_extra_spaces(self):
        """Тест вывода с лишними пробелами - они должны игнорироваться"""
        helper = TestHelper("", "  hello  \n  world  ")
        result = helper.output("hello\nworld")
        assert result is True
    
    def test_output_partial_match_include_true(self):
        """Тест частичного совпадения с include=True"""
        helper = TestHelper("", "hello world test")
        result = helper.output("world", include=True)
        assert result is True
    
    def test_output_partial_match_include_false(self):
        """Тест частичного совпадения с include=False (по умолчанию)"""
        helper = TestHelper("", "hello world test")
        result = helper.output("world", include=False)
        assert isinstance(result, str)
        assert "Фактический вывод" in result
    
    def test_output_no_match(self):
        """Тест несовпадающего вывода"""
        helper = TestHelper("", "hello")
        result = helper.output("world")
        assert isinstance(result, str)
        assert "Фактический вывод" in result
    
    def test_output_empty_stdout(self):
        """Тест пустого вывода"""
        helper = TestHelper("", "")
        result = helper.output("hello")
        assert isinstance(result, str)
        assert "Фактический вывод" in result
    
    def test_output_custom_message(self):
        """Тест с пользовательским сообщением об ошибке"""
        helper = TestHelper("", "hello")
        result = helper.output("world", msg="Неправильный вывод")
        assert result == "Неправильный вывод"


class TestTestHelperContains:
    """Тесты для метода contains() класса TestHelper"""
    
    def test_contains_simple_string(self):
        """Тест простого поиска строки"""
        helper = TestHelper("x = 1\ny = 2", "")
        result = helper.contains("x = 1")
        assert result is True
    
    def test_contains_with_spaces(self):
        """Тест поиска с пробелами - пробелы должны игнорироваться"""
        helper = TestHelper("x = 1", "")
        result = helper.contains("x=1")
        assert result is True
    
    def test_contains_with_quotes(self):
        """Тест поиска с кавычками - одинарные и двойные кавычки должны нормализоваться"""
        helper = TestHelper('name = "John"', "")
        result = helper.contains("name='John'")
        assert result is True
    
    def test_contains_multiline(self):
        """Тест поиска многострочного кода"""
        helper = TestHelper("if x > 0:\n    print('positive')", "")
        result = helper.contains("if x > 0:\n    print('positive')")
        assert result is True
    
    def test_contains_not_found(self):
        """Тест поиска несуществующей строки"""
        helper = TestHelper("x = 1", "")
        result = helper.contains("y = 2")
        assert isinstance(result, str)
        assert "Ожидается" in result
    
    def test_contains_custom_message(self):
        """Тест с пользовательским сообщением об ошибке"""
        helper = TestHelper("x = 1", "")
        result = helper.contains("y = 2", msg="Код должен содержать y = 2")
        assert result == "Код должен содержать y = 2"


class TestTestHelperIntegration:
    """Интеграционные тесты для класса TestHelper"""
    
    def test_multiple_checks_same_helper(self):
        """Тест множественных проверок с одним экземпляром TestHelper"""
        helper = TestHelper("x = 10\nprint(x)", "10")
        
        # Проверяем переменную
        var_result = helper.var("x", 10)
        assert var_result is True
        
        # Проверяем вызов функции
        call_result = helper.call("print")
        assert call_result is True
        
        # Проверяем вывод
        output_result = helper.output("10")
        assert output_result is True
    
    def test_helper_with_complex_code(self):
        """Тест с комплексным кодом"""
        code = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3]})
result = df.head()
print(result)
"""
        helper = TestHelper(code, "   A\n0  1\n1  2\n2  3")
        
        # Проверяем импорт
        contains_result = helper.contains("import pandas as pd")
        assert contains_result is True
        
        # Проверяем создание DataFrame
        var_result = helper.var("df", "pd.DataFrame({'A':[1,2,3]})")
        assert var_result is True
        
        # Проверяем вызов метода
        call_result = helper.call("head")
        assert call_result is True
