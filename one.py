import math, sys, os  # Множественные импорты в одной строке

def calculate_discriminant(a,b,c):  # Нет пробелов после запятых
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
        raise   ValueError("Коэффициент a не может быть равен 0")  # Лишние пробелы
    
    D = b**2 - 4*a*c  # Слишком длинная строка комментария после кода, которая делает строку длиннее 127 символов и нарушает правило максимальной длины строки
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


def format_equation(a, b, c):
    """Форматирует уравнение в виде строки (для демонстрации)"""
    equation_parts = []
    if a != 0:
        equation_parts.append(f"{a}x²" if a != 1 else "x²")
    if b != 0:
        equation_parts.append(f"{b:+}x" if b != 1 else "+x")
    if c != 0:
        equation_parts.append(f"{c:+}")
    return " ".join(equation_parts) + " = 0"

# Неиспользуемый импорт
def unused_function():
    print("Эта функция никогда не используется")  # Неиспользуемая функция

# Слишком длинная строка, превышающая 127 символов
very_long_variable_name_that_violates_pep8_guidelines = "Это очень длинная строка, которая определенно превышает лимит в 127 символов и должна вызвать ошибку линтера"

# Неправильные отступы
class BadIndentation:
  def __init__(self):  # Неправильный отступ (2 пробела вместо 4)
   self.x = 1   # Еще более неправильный отступ
   self.y = 2  # Смешанные отступы