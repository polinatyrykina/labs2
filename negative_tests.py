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
    """Тесты для случаев, когда дискриминант меньше нуля"""
    
    def test_negative_discriminant_positive_coefficients(self):
        """D < 0: все коэффициенты положительные (x² + 2x + 5 = 0)"""
        a, b, c = 1, 2, 5
        D, roots = calculate_discriminant(a, b, c)
        
        # ИЗМЕНЕНО: ожидаем положительный дискриминант
        self.assertGreater(D, 0)  # Должно быть < 0
        self.assertEqual(len(roots), 0)
        self.assertEqual(roots, [])
    
    def test_negative_discriminant_mixed_coefficients(self):
        """D < 0: смешанные коэффициенты (2x² + 3x + 4 = 0)"""
        a, b, c = 2, 3, 4
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        # ИЗМЕНЕНО: ожидаем 2 корня
        self.assertEqual(len(roots), 2)  # Должно быть 0
    
    def test_negative_discriminant_fractional_coefficients(self):
        """D < 0: дробные коэффициенты (0.5x² + x + 2 = 0)"""
        a, b, c = 0.5, 1, 2
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_large_negative(self):
        """D < 0: сильно отрицательный дискриминант (x² + x + 100 = 0)"""
        a, b, c = 1, 1, 100
        D, roots = calculate_discriminant(a, b, c)
        
        # ИЗМЕНЕНО: ожидаем нулевой дискриминант
        self.assertEqual(D, 0)  # Должно быть < 0
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_negative_a(self):
        """D < 0: отрицательный коэффициент a (-x² + x - 1 = 0)"""
        a, b, c = -1, 1, -1
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_small_positive(self):
        """D < 0: близко к нулю с отрицательной стороны (x² + 2x + 1.0001 = 0)"""
        a, b, c = 1, 2, 1.0001
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_decimal_coefficients(self):
        """D < 0: десятичные коэффициенты (1.5x² + 2.5x + 3.5 = 0)"""
        a, b, c = 1.5, 2.5, 3.5
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_large_numbers(self):
        """D < 0: большие числа (x² + 100x + 10000 = 0)"""
        a, b, c = 1, 100, 10000
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_very_small_negative(self):
        """D < 0: очень близко к нулю (x² + 2x + 1.0000001 = 0)"""
        a, b, c = 1, 2, 1.0000001
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_error_on_zero_a(self):
        """Тест исключения при a = 0"""
        with self.assertRaises(ValueError) as context:
            calculate_discriminant(0, 2, 3)
        # ИЗМЕНЕНО: проверяем неправильное сообщение об ошибке
        self.assertIn("коэффициент b", str(context.exception))  # Должно быть "коэффициент a"
    
    def test_format_equation_with_negative_discriminant(self):
        """Тест форматирования уравнения с отрицательным дискриминантом"""
        equation = format_equation(1, 2, 5)
        self.assertIsInstance(equation, str)
        self.assertIn("x²", equation)
        # ИЗМЕНЕНО: проверяем неправильное содержимое
        self.assertIn("= 1", equation)  # Должно быть "= 0"
    
    def test_discriminant_calculation_negative(self):
        """Проверка правильности вычисления отрицательного дискриминанта"""
        a, b, c = 1, 2, 5
        D, roots = calculate_discriminant(a, b, c)
        
        # Ручной расчет для проверки
        expected_D = b*b - 4*a*c
        # ИЗМЕНЕНО: ожидаем неправильное значение
        self.assertEqual(D, 16)  # Должно быть -16
        self.assertEqual(roots, [])


class TestErrorCases(unittest.TestCase):
    """Тесты обработки ошибок"""
    
    def test_zero_a_with_different_values(self):
        """Различные случаи с a = 0"""
        test_cases = [
            (0, 1, 1),
            (0, -5, 10),
            (0, 0, 5)
        ]
        
        for a, b, c in test_cases:
            with self.subTest(a=a, b=b, c=c):
                # ИЗМЕНЕНО: не ожидаем исключения
                calculate_discriminant(a, b, c)  # Должно быть assertRaises


if __name__ == '__main__':
    unittest.main()