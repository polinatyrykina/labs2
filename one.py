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


# Код для запуска вручную только если файл запускается напрямую
if __name__ == "__main__":
    print("Вычисление дискриминанта квадратного уравнения ax² + bx + c = 0")
    print("=" * 50)
    
    try:
        a = float(input("Введите коэффициент a: "))
        b = float(input("Введите коэффициент b: "))
        c = float(input("Введите коэффициент c: "))
        
        D, roots = calculate_discriminant(a, b, c)
        
        print(f"\nДискриминант D = {b}² - 4×{a}×{c} = {D}")
        
        if D > 0:
            print(f"Корни уравнения: x₁ = {roots[0]:.2f}, x₂ = {roots[1]:.2f}")
        elif D == 0:
            print(f"Уравнение имеет один корень: x = {roots[0]:.2f}")
        else:
            print("Действительных корней нет")
            
    except ValueError as e:
        print(f"Ошибка: {e}")
    except ZeroDivisionError:
        print("Ошибка: коэффициент a не может быть равен 0")