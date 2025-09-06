"""
Конфигурация pytest для тестов cupychecker
"""
import pytest
import sys
import os

# Добавляем путь к модулю cupychecker в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cupychecker'))

@pytest.fixture
def sample_code():
    """Фикстура с примером кода для тестирования"""
    return """
x = 10
y = "hello"
print(x)
"""

@pytest.fixture
def sample_stdout():
    """Фикстура с примером вывода для тестирования"""
    return "10"

@pytest.fixture
def complex_code():
    """Фикстура с комплексным кодом для тестирования"""
    return """
import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
result = df.head(2)
print(result)
"""

@pytest.fixture
def complex_stdout():
    """Фикстура с комплексным выводом для тестирования"""
    return "   A  B\n0  1  4\n1  2  5"
