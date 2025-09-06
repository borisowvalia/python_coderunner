"""
Тесты для модуля checker библиотеки cupychecker
"""
import pytest
from unittest.mock import Mock, patch
import requests
from cupychecker.checker import run_code, check_result


class TestRunCode:
    """Тесты для функции run_code()"""
    
    @patch('cupychecker.checker.requests.post')
    def test_run_code_success(self, mock_post):
        """Тест успешного выполнения кода"""
        # Настраиваем мок
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "output": "hello"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Выполняем тест
        result = run_code("print('hello')")
        
        # Проверяем результат
        assert result == {"result": "success", "output": "hello"}
        mock_post.assert_called_once_with(
            'http://localhost:8000/run',
            json={'code': "print('hello')"}
        )
    
    @patch('cupychecker.checker.requests.post')
    def test_run_code_custom_host(self, mock_post):
        """Тест с пользовательским хостом"""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = run_code("print('hello')", host='http://example.com:9000')
        
        assert result == {"result": "success"}
        mock_post.assert_called_once_with(
            'http://example.com:9000/run',
            json={'code': "print('hello')"}
        )
    
    @patch('cupychecker.checker.requests.post')
    def test_run_code_http_error(self, mock_post):
        """Тест обработки HTTP ошибки"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("500 Internal Server Error")
        mock_post.return_value = mock_response
        
        with pytest.raises(requests.HTTPError):
            run_code("print('hello')")


class TestCheckResult:
    """Тесты для функции check_result()"""
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_local_success(self, mock_load_local):
        """Тест успешной проверки с локальными конфигурациями"""
        # Настраиваем мок для локальной загрузки
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                }
            ]
        }
        
        # Выполняем тест
        result = check_result("x = 10", "", module=1, task=1)
        
        # Проверяем результат
        assert result is True
        mock_load_local.assert_called_once_with(module=1, task=1)
    
    @patch('cupychecker.checker.load_remote')
    def test_check_result_remote_success(self, mock_load_remote):
        """Тест успешной проверки с удаленными конфигурациями"""
        # Настраиваем мок для удаленной загрузки
        mock_load_remote.return_value = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                }
            ]
        }
        
        # Выполняем тест
        result = check_result("x = 10", "", module=1, task=1, host='http://example.com')
        
        # Проверяем результат
        assert result is True
        mock_load_remote.assert_called_once_with(module=1, task=1, host='http://example.com')
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_var_failure(self, mock_load_local):
        """Тест неудачной проверки переменной"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                }
            ]
        }
        
        result = check_result("x = 5", "", module=1, task=1)
        
        assert isinstance(result, str)
        assert "было переписвоено значение 5" in result
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_call_success(self, mock_load_local):
        """Тест успешной проверки вызова функции"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'call',
                    'expected': {'func': 'print', 'args': [123]}
                }
            ]
        }
        
        result = check_result("print(123)", "", module=1, task=1)
        
        assert result is True
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_call_failure(self, mock_load_local):
        """Тест неудачной проверки вызова функции"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'call',
                    'expected': {'func': 'print', 'args': [123]}
                }
            ]
        }
        
        result = check_result("x = 1", "", module=1, task=1)
        
        assert isinstance(result, str)
        assert "Не найден вызов функции" in result
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_output_success(self, mock_load_local):
        """Тест успешной проверки вывода"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'output',
                    'expected': {'stdout': 'hello'}
                }
            ]
        }
        
        result = check_result("print('hello')", "hello", module=1, task=1)
        
        assert result is True
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_output_failure(self, mock_load_local):
        """Тест неудачной проверки вывода"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'output',
                    'expected': {'stdout': 'hello'}
                }
            ]
        }
        
        result = check_result("print('world')", "world", module=1, task=1)
        
        assert isinstance(result, str)
        assert "Фактический вывод" in result
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_contains_success(self, mock_load_local):
        """Тест успешной проверки содержания кода"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'contains',
                    'expected': {'code': 'import pandas'}
                }
            ]
        }
        
        result = check_result("import pandas as pd", "", module=1, task=1)
        
        assert result is True
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_contains_failure(self, mock_load_local):
        """Тест неудачной проверки содержания кода"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'contains',
                    'expected': {'code': 'import pandas'}
                }
            ]
        }
        
        result = check_result("import numpy as np", "", module=1, task=1)
        
        assert isinstance(result, str)
        assert "Ожидается" in result
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_multiple_checks_all_pass(self, mock_load_local):
        """Тест множественных проверок - все проходят"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                },
                {
                    'type': 'call',
                    'expected': {'func': 'print'}
                },
                {
                    'type': 'output',
                    'expected': {'stdout': '10'}
                }
            ]
        }
        
        result = check_result("x = 10\nprint(x)", "10", module=1, task=1)
        
        assert result is True
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_multiple_checks_first_fails(self, mock_load_local):
        """Тест множественных проверок - первая не проходит"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                },
                {
                    'type': 'call',
                    'expected': {'func': 'print'}
                }
            ]
        }
        
        result = check_result("x = 5\nprint(x)", "5", module=1, task=1)
        
        assert isinstance(result, str)
        assert "было переписвоено значение 5" in result
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_with_custom_messages(self, mock_load_local):
        """Тест с пользовательскими сообщениями об ошибках"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10},
                    'message': 'Переменная x должна быть равна 10'
                }
            ]
        }
        
        result = check_result("x = 5", "", module=1, task=1)
        
        assert result == 'Переменная x должна быть равна 10'
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_output_with_include(self, mock_load_local):
        """Тест проверки вывода с параметром include"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'output',
                    'expected': {'stdout': 'hello', 'include': True}
                }
            ]
        }
        
        result = check_result("print('hello world')", "hello world", module=1, task=1)
        
        assert result is True
    
    @patch('cupychecker.checker.load_local')
    def test_check_result_call_without_args(self, mock_load_local):
        """Тест проверки вызова функции без аргументов"""
        mock_load_local.return_value = {
            'checks': [
                {
                    'type': 'call',
                    'expected': {'func': 'print'}
                }
            ]
        }
        
        result = check_result("print()", "", module=1, task=1)
        
        assert result is True
