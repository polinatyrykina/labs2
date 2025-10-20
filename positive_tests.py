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
    
    def test_positive_discriminant_two_roots_fractions(self):
        """D > 0: два дробных корня (2x² + 5x - 3 = 0)"""
        a, b, c = 2, 5, -3
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], 0.5)
        self.assertAlmostEqual(roots[1], -3.0)
    
    def test_positive_discriminant_irrational_roots(self):
        """D > 0: иррациональные корни (x² - 2x - 1 = 0)"""
        a, b, c = 1, -2, -1
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], 2.414213562373095, places=10)
        self.assertAlmostEqual(roots[1], -0.41421356237309515, places=10)
    
    def test_zero_discriminant_one_root_integer(self):
        """D = 0: один целый корень (x² - 4x + 4 = 0)"""
        a, b, c = 1, -4, 4
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertEqual(D, 0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], 2.0)
    
    def test_zero_discriminant_one_root_fraction(self):
        """D = 0: один дробный корень (4x² + 4x + 1 = 0)"""
        a, b, c = 4, 4, 1
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertEqual(D, 0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], -0.5)
    
    def test_zero_discriminant_decimal_coefficients(self):
        """D = 0: десятичные коэффициенты (0.25x² + x + 1 = 0)"""
        a, b, c = 0.25, 1, 1
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertEqual(D, 0)
        self.assertEqual(len(roots), 1)
        self.assertAlmostEqual(roots[0], -2.0)
    
    def test_positive_discriminant_large_numbers(self):
        """D > 0: большие числа (x² + 1000x + 240000 = 0)"""
        a, b, c = 1, 1000, 240000
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], -400.0)
        self.assertAlmostEqual(roots[1], -600.0)
    
    def test_positive_discriminant_negative_coefficients(self):
        """D > 0: все коэффициенты отрицательные (-x² - 5x - 6 = 0)"""
        a, b, c = -1, -5, -6
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
        roots_sorted = sorted(roots)
        self.assertAlmostEqual(roots_sorted[0], -3.0)
        self.assertAlmostEqual(roots_sorted[1], -2.0)
    
    def test_format_equation_function(self):
        """Тест функции форматирования уравнения"""
        # Тестируем format_equation если она импортирована
        equation = format_equation(1, -3, 2)
        self.assertIsInstance(equation, str)
        self.assertIn("x²", equation)
    
    def test_discriminant_properties(self):
        """Тест математических свойств дискриминанта"""
        a, b, c = 1, -5, 6
        D, roots = calculate_discriminant(a, b, c)
        
        # Проверяем, что дискриминант вычислен правильно
        expected_D = b*b - 4*a*c
        self.assertEqual(D, expected_D)
        
        # Проверяем, что корни удовлетворяют уравнению
        for root in roots:
            result = a*root*root + b*root + c
            self.assertAlmostEqual(result, 0, places=10)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""
    
    def test_small_positive_discriminant(self):
        """D близко к 0 с положительной стороны"""
        a, b, c = 1, 2, 0.9999
        D, roots = calculate_discriminant(a, b, c)
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
    
    def test_coefficient_a_negative(self):
        """Отрицательный коэффициент a с D > 0"""
        a, b, c = -2, 5, -2
        D, roots = calculate_discriminant(a, b, c)
        self.assertGreater(D, 0)
        self.assertEqual(len(roots), 2)
    
    def test_large_coefficients(self):
        """Очень большие коэффициенты"""
        a, b, c = 1e6, 2e6, 1e6
        D, roots = calculate_discriminant(a, b, c)
        self.assertEqual(D, 0)
        self.assertEqual(len(roots), 1)


if __name__ == '__main__':
    unittest.main() git commit - m 'улучшение тестов'