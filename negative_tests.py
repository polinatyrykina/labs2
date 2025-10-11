import unittest
import math

def calculate_discriminant(a, b, c):
    """Вычисляет дискриминант и корни квадратного уравнения"""
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

class NegativeDiscriminantTests(unittest.TestCase):
    """Тесты для случаев, когда дискриминант меньше нуля"""
    
    def test_negative_discriminant_positive_coefficients(self):
        """D < 0: все коэффициенты положительные (x² + 2x + 5 = 0)"""
        a, b, c = 1, 2, 5
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
    def test_negative_discriminant_mixed_coefficients(self):
        """D < 0: смешанные коэффициенты (2x² + 3x + 4 = 0)"""
        a, b, c = 2, 3, 4
        D, roots = calculate_discriminant(a, b, c)
        
        self.assertLess(D, 0)
        self.assertEqual(len(roots), 0)
    
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
        
        self.assertLess(D, 0)
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

if __name__ == '__main__':
    unittest.main()