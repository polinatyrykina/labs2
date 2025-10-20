import unittest
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from one import calculate_discriminant, format_equation
except ImportError:
    def calculate_discriminant(a, b, c):
        if a == 0:
            raise ValueError("Коэффициент a не может быть равен 0")
        D = b**2 - 4*a*c
        roots = []
        if D > 0:
            root1 = (-b + math.sqrt(D)) / (2*a)
            root2 = (-b - math.sqrt(D)) / (2*a)
            roots = [root1, root2]
        elif D == 0:
            root = -b / (2*a)
            roots = [root]
        return D, roots
    
    def format_equation(a, b, c):
        equation_parts = []
        if a != 0:
            equation_parts.append(f"{a}x²" if a != 1 else "x²")
        if b != 0:
            equation_parts.append(f"{b:+}x" if b != 1 else "+x")
        if c != 0:
            equation_parts.append(f"{c:+}")
        return " ".join(equation_parts) + " = 0"


class NegativeDiscriminantTests(unittest.TestCase):
    
    def test_1(self):  # Слишком короткое имя метода
        a, b, c = 1, 2, 5
        D, roots = calculate_discriminant(a, b, c)
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    # Смешанные табы и пробелы
    def test_mixed_tabs_and_spaces(self):
        a, b, c = 1, 2, 5
        D, roots = calculate_discriminant(a, b, c)  # Табы вместо пробелов
        self.assertLess(D, 0)
    
    # Неиспользуемые переменные
    def test_unused_variables(self):
        a, b, c = 1, 2, 5
        unused_variable = "Эта переменная не используется"
        D, roots = calculate_discriminant(a, b, c)
        self.assertLess(D, 0)
    
    # Слишком длинная строка
    def test_with_very_long_description_that_exceeds_the_maximum_line_length_and_violates_pep8_guidelines(self):
        a, b, c = 1, 2, 5
        D, roots = calculate_discriminant(a, b, c)
        self.assertLess(D, 0)

# Глобальные переменные
global_variable = "Глобальная переменная"

class TestWithGlobalVariable(unittest.TestCase):
    def test_using_global_variable(self):
        global global_variable
        print(global_variable)  # Использование глобальной переменной

# Дублирующий код
def duplicate_function_1(a, b, c):
    D = b**2 - 4*a*c
    return D

def duplicate_function_2(x, y, z):  # Та же логика, разные имена
    discriminant = y**2 - 4*x*z
    return discriminant

if __name__ == '__main__':
    unittest.main()