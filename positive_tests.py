import unittest
import math

import unittest
import math
import sys
import os

# Добавляем путь к текущей директории для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем функцию из файла 1.py
try:
    from one.py import calculate_discriminant 
except ImportError:
        import importlib.util
        spec = importlib.util.spec_from_file_location("discriminant_module", "one.py")
        discriminant_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(discriminant_module)
        calculate_discriminant = discriminant_module.calculate_discriminant


# def calculate_discriminant(a, b, c):
#     """Вычисляет дискриминант и корни квадратного уравнения"""
#     if a == 0:
#         raise ValueError("Коэффициент a не может быть равен 0")
    
#     D = b**2 - 4*a*c
#     roots = []
    
#     if D > 0:
#         root1 = (-b + math.sqrt(D)) / (2*a)
#         root2 = (-b - math.sqrt(D)) / (2*a)
#         roots = [root1, root2]
#     elif D == 0:
#         root = -b / (2*a)
#         roots = [root]
    
#     return D, roots

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

if __name__ == '__main__':
    unittest.main()