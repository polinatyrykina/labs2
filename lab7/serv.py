from flask import Flask, jsonify
import sys

app = Flask(__name__)

# Получаем порт 
if len(sys.argv) < 2:
    print("Usage: python server.py <port>")
    sys.exit(1)

PORT = int(sys.argv[1])
INSTANCE_ID = f"instance_{PORT}"

@app.route('/health', methods=['GET'])
def health():
    """Эндпоинт для проверки состояния инстанса"""
    return jsonify({
        "status": "healthy",
        "instance_id": INSTANCE_ID,
        "port": PORT
    })

@app.route('/process', methods=['GET', 'POST'])
def process():
    """Эндпоинт для обработки запросов"""
    return jsonify({
        "message": "Request processed successfully",
        "instance_id": INSTANCE_ID,
        "port": PORT
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)