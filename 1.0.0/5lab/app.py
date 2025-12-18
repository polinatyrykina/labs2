from flask_login import UserMixin
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor

# Инициализация приложения Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '111222333'

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname="razrab-labs1",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    return conn

# Функция для создания таблиц
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Создание таблицы пользователей
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL,
            name VARCHAR(100) NOT NULL
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

# Создаем таблицы при запуске
create_tables()

# Маршрут для корневой страницы
@app.route('/')
def index():
    if 'user_id' in session:
        # Получаем данные пользователя из базы
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            return render_template('index.html', user=user)
    
    return redirect(url_for('login'))

# Маршрут для страницы входа (GET и POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        # Получение данных из формы
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Проверка обязательных полей
        if not email or not password:
            error = 'Все поля обязательны для заполнения'
            return render_template('login.html', error=error)
        
        # Поиск пользователя по email
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        # Проверка существования пользователя
        if not user:
            error = 'Пользователь с таким email не найден'
            return render_template('login.html', error=error)
        
        # Проверка пароля
        if not check_password_hash(user['password'], password):
            error = 'Неверный пароль'
            return render_template('login.html', error=error)
        
        # Успешная авторизация
        session['user_id'] = user['id']
        return redirect(url_for('index'))
    
    # GET запрос - отображение формы входа
    return render_template('login.html', error=error)

# Маршрут для страницы регистрации (GET и POST)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    
    if request.method == 'POST':
        # Получение данных из формы
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Проверка обязательных полей
        if not name or not email or not password:
            error = 'Все поля обязательны для заполнения'
            return render_template('signup.html', error=error)
        
        # Проверка существования пользователя с таким email
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        
        if existing_user:
            error = 'Пользователь с таким email уже существует'
            cur.close()
            conn.close()
            return render_template('signup.html', error=error)
        
        # Создание нового пользователя с хешированным паролем
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        
        # Сохранение пользователя в базе данных
        conn.commit()
        cur.close()
        conn.close()
        
        success = 'Регистрация успешна! Теперь вы можете войти.'
        return render_template('signup.html', success=success)
    
    # GET запрос - отображение формы регистрации
    return render_template('signup.html', error=error, success=success)

# Маршрут для выхода из системы
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
    
    