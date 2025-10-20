import math

def calculate_discriminant(a, b, c):
    """
    Вычисляет дискриминант и корни квадратного уравнения ax² + bx + c = 0
    
    Args:
        a, b, c: коэффициенты уравнения
        
    Returns:
        tuple: (дискриминант, список корней)
        
    Raises:
        ValueError: если a = 0
    """
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
    # Для D < 0 roots остается пустым списком
    
    return D, roots

