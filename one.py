def calculate_discriminant(a, b, c):
    return b ** 2 - 4 * a * c

if __name__ == "__main__":
    try:
        a = float(input("Введите коэффициент a: "))
        b = float(input("Введите коэффициент b: "))
        c = float(input("Введите коэффициент c: "))
        discriminant = calculate_discriminant(a, b, c)
        print(f"Дискриминант: {discriminant}")
    except ValueError:
        print("Ошибка: введите числовые значения коэффициентов.")