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
    
    def test_check_result_local_success(self):
        """Тест успешной проверки с локальными конфигурациями (task_conf напрямую)"""
        task_conf = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                }
            ]
        }

        result = check_result("x = 10", "", task_conf=task_conf)

        assert result is True
    
    def test_check_result_remote_success(self):
        """Тест успешной проверки с конфигурациями, полученными извне (эмуляция remote)"""
        task_conf = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                }
            ]
        }

        result = check_result("x = 10", "", task_conf=task_conf, host='http://example.com')

        assert result is True
    
    def test_check_result_var_failure(self):
        """Тест неудачной проверки переменной"""
        task_conf = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10}
                }
            ]
        }

        result = check_result("x = 5", "", task_conf=task_conf)
        
        assert isinstance(result, str)
        assert "было переписвоено значение 5" in result
    
    def test_check_result_call_success(self):
        """Тест успешной проверки вызова функции"""
        task_conf = {
            'checks': [
                {
                    'type': 'call',
                    'expected': {'func': 'print', 'args': [123]}
                }
            ]
        }

        result = check_result("print(123)", "", task_conf=task_conf)
        
        assert result is True
    
    def test_check_result_call_failure(self):
        """Тест неудачной проверки вызова функции"""
        task_conf = {
            'checks': [
                {
                    'type': 'call',
                    'expected': {'func': 'print', 'args': [123]}
                }
            ]
        }

        result = check_result("x = 1", "", task_conf=task_conf)
        
        assert isinstance(result, str)
        assert "Не найден вызов функции" in result
    
    def test_check_result_output_success(self):
        """Тест успешной проверки вывода"""
        task_conf = {
            'checks': [
                {
                    'type': 'output',
                    'expected': {'stdout': 'hello'}
                }
            ]
        }

        result = check_result("print('hello')", "hello", task_conf=task_conf)
        
        assert result is True
    
    def test_check_result_output_failure(self):
        """Тест неудачной проверки вывода"""
        task_conf = {
            'checks': [
                {
                    'type': 'output',
                    'expected': {'stdout': 'hello'}
                }
            ]
        }

        result = check_result("print('world')", "world", task_conf=task_conf)
        
        assert isinstance(result, str)
        assert "Фактический вывод" in result
    
    def test_check_result_contains_success(self):
        """Тест успешной проверки содержания кода"""
        task_conf = {
            'checks': [
                {
                    'type': 'contains',
                    'expected': {'code': 'import pandas'}
                }
            ]
        }

        result = check_result("import pandas as pd", "", task_conf=task_conf)
        
        assert result is True
    
    def test_check_result_contains_failure(self):
        """Тест неудачной проверки содержания кода"""
        task_conf = {
            'checks': [
                {
                    'type': 'contains',
                    'expected': {'code': 'import pandas'}
                }
            ]
        }

        result = check_result("import numpy as np", "", task_conf=task_conf)
        
        assert isinstance(result, str)
        assert "Ожидается" in result
    
    def test_check_result_multiple_checks_all_pass(self):
        """Тест множественных проверок - все проходят"""
        task_conf = {
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

        result = check_result("x = 10\nprint(x)", "10", task_conf=task_conf)
        
        assert result is True
    
    def test_check_result_multiple_checks_first_fails(self):
        """Тест множественных проверок - первая не проходит"""
        task_conf = {
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

        result = check_result("x = 5\nprint(x)", "5", task_conf=task_conf)
        
        assert isinstance(result, str)
        assert "было переписвоено значение 5" in result
    
    def test_check_result_with_custom_messages(self):
        """Тест с пользовательскими сообщениями об ошибках"""
        task_conf = {
            'checks': [
                {
                    'type': 'var',
                    'expected': {'var': 'x', 'value': 10},
                    'message': 'Переменная x должна быть равна 10'
                }
            ]
        }

        result = check_result("x = 5", "", task_conf=task_conf)
        
        assert result == 'Переменная x должна быть равна 10'
    
    def test_check_result_output_with_include(self):
        """Тест проверки вывода с параметром include"""
        task_conf = {
            'checks': [
                {
                    'type': 'output',
                    'expected': {'stdout': 'hello', 'include': True}
                }
            ]
        }

        result = check_result("print('hello world')", "hello world", task_conf=task_conf)
        
        assert result is True
    
    def test_check_result_call_without_args(self):
        """Тест проверки вызова функции без аргументов"""
        task_conf = {
            'checks': [
                {
                    'type': 'call',
                    'expected': {'func': 'print'}
                }
            ]
        }

        result = check_result("print()", "", task_conf=task_conf)
        
        assert result is True
