from flask import Flask, request, jsonify
import json
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)


# Инициализация Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="memory://"
)

# Путь к файлу данных
DATA_FILE = 'data.json'

# Загрузка данных при старте приложения
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

data = load_data()

def save_data():
    """Сохранить данные в файл"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        return False

@app.route('/set', methods=['POST'])
@limiter.limit("10 per minute")
def set_key():
    """Сохранить ключ-значение"""
    try:
        # Получаем JSON из запроса
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                "error": "Требуется JSON данные",
                "status": "error"
            }), 400
        
        # Проверяем наличие ключа
        if 'key' not in request_data:
            return jsonify({
                "error": "Ключ 'key' обязателен",
                "status": "error"
            }), 400
        
        key = request_data['key']
        value = request_data.get('value')
        
        # Сохраняем в словарь
        data[key] = value
        
        # Сохраняем в файл
        if save_data():
            return jsonify({
                "message": f"Ключ '{key}' сохранен",
                "status": "success"
            }), 200
        else:
            return jsonify({
                "error": "Ошибка при сохранении данных",
                "status": "error"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Внутренняя ошибка сервера: {str(e)}",
            "status": "error"
        }), 500

@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    """Получить значение по ключу"""
    try:
        if key in data:
            return jsonify({
                "key": key,
                "value": data[key],
                "status": "success"
            }), 200
        else:
            return jsonify({
                "error": f"Ключ '{key}' не найден",
                "status": "error"
            }), 404
    except Exception as e:
        return jsonify({
            "error": f"Внутренняя ошибка сервера: {str(e)}",
            "status": "error"
        }), 500

@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete_key(key):
    """Удалить ключ"""
    try:
        if key in data:
            # Удаляем ключ
            del data[key]
            
            # Сохраняем в файл
            if save_data():
                return jsonify({
                    "message": f"Ключ '{key}' удален",
                    "status": "success"
                }), 200
            else:
                return jsonify({
                    "error": "Ошибка при сохранении данных",
                    "status": "error"
                }), 500
        else:
            return jsonify({
                "error": f"Ключ '{key}' не найден",
                "status": "error"
            }), 404
    except Exception as e:
        return jsonify({
            "error": f"Внутренняя ошибка сервера: {str(e)}",
            "status": "error"
        }), 500

@app.route('/exists/<key>', methods=['GET'])
def exists_key(key):
    """Проверить наличие ключа"""
    try:
        exists = key in data
        return jsonify({
            "key": key,
            "exists": exists,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Внутренняя ошибка сервера: {str(e)}",
            "status": "error"
        }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Обработчик превышения лимита запросов"""
    return jsonify({
        "error": "Превышен лимит запросов",
        "status": "error",
        "detail": str(e.description)
    }), 429

@app.route('/keys', methods=['GET'])
def get_all_keys():
    """Возвращает все ключи из хранилища"""
    return jsonify({
        'success': True,
        'keys': list(data.keys()),
        'count': len(data)
        }), 200
# Корневой маршрут

@app.route('/')
def index():
    return jsonify({
        'message': 'Key-Value Storage API',
        'endpoints': {
            'POST /set': 'Save key-value pair',
            'GET /get/<key>': 'Get value by key',
            'DELETE /delete/<key>': 'Delete key',
            'GET /exists/<key>': 'Check if key exists',
            'GET /keys': 'Get all keys'
        },
        'total_keys': len(data)
    })

if __name__ == '__main__':
    print(f"Key-Value хранилище запущено")
    print(f"Данные загружены из {DATA_FILE}: {len(data)} записей")
    print(f"Общий лимит: 100 запросов в сутки")
    print(f"Лимиты для /set и /delete: 10 запросов в минуту")
    print(f"  Главная страница: http://127.0.0.1:5000/")
    print(f"  Получить значение: http://127.0.0.1:5000/get/<ключ>")
    print(f"  Проверить ключ:   http://127.0.0.1:5000/exists/<ключ>")
    print(f"  Все ключи:        http://127.0.0.1:5000/keys")
    app.run(debug=True, host='0.0.0.0', port=5000)
