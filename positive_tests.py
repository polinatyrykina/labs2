import unittest
import math
import os
import sys

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем функции из one.py
try:
    from one import calculate_discriminant, format_equation
except ImportError:
    # Fallback функции
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


class PositiveDiscriminantTests(unittest.TestCase):
    """Тесты для случаев, когда дискриминант больше или равен нулю"""
    
    def test_positive_discriminant_two_roots_integers(self):
        """D > 0: два целых корня (x² - 3x + 2 = 0)"""
        a, b, c = 1, -3, 2
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], 2.0)
        self.assertAlmostEqual(roots[1], 1.0)
    
    # Слишком длинное имя метода, нарушающее стиль
    def test_positive_discriminant_with_very_long_method_name_that_violates_pep8_guidelines(self):
        """D > 0: тест с очень длинным именем метода"""
        a, b, c = 1, -3, 2
        D, roots = calculate_discriminant(a, b, c)
        self.assertGreater(D, 0)

    # Неправильные пробелы
    def test_bad_spacing( self ):  # Лишние пробелы вокруг self
        a,b,c=1,-3,2  # Нет пробелов после запятых и вокруг операторов
        D,roots=calculate_discriminant(a,b,c)
        self.assertTrue(D>0)  # Нет пробелов вокруг оператора

    # Использование assert вместо специализированных методов
    def test_using_assert_instead_of_specialized_methods(self):
        a, b, c = 1, -3, 2
        D, roots = calculate_discriminant(a, b, c)
        assert D > 0  # Использование assert вместо self.assertGreater
        assert len(roots) == 2  # Использование assert вместо self.assertEqual

# Пустые классы и методы
class EmptyClass:
    pass

def empty_function():
    """Пустая функция без реализации"""
    pass

# Слишком сложная функция (высокая цикломатическая сложность)
def very_complex_function(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                return "even small positive"
            else:
                return "odd small positive"
        elif x < 100:
            if x % 2 == 0:
                return "even medium positive"
            else:
                return "odd medium positive"
        else:
            if x % 2 == 0:
                return "even large positive"
            else:
                return "odd large positive"
    elif x < 0:
        if x > -10:
            if x % 2 == 0:
                return "even small negative"
            else:
                return "odd small negative"
        else:
            if x % 2 == 0:
                return "even large negative"
            else:
                return "odd large negative"
    else:
        return "zero"

if __name__ == '__main__':
    unittest.main()