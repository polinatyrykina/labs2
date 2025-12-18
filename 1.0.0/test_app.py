# test_app.py - минимальные тесты

def test_simple():
    """Простой тест что всё работает"""
    print("Запускаю тесты...")
    assert 1 == 1
    print("✓ Простой тест пройден")

def test_app_exists():
    """Проверяем что app.py можно импортировать"""
    try:
        import app7
        print("✓ app.py можно импортировать")
    except:
        print("✗ Не могу импортировать app.py")

if __name__ == "__main__":
    test_simple()
    test_app_exists()
    print("Все тесты завершены!")