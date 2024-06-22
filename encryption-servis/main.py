from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import time
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Определение поддерживаемого алфавита для шифров
ALPHABET = " ,.:(_)-0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Хранение данных в памяти для пользователей, методов и сессий
users = []
methods = []
sessions = []

# Вспомогательные функции

def vigenere_cipher(text, key, encrypt=True):
    """
    Функция шифрования/дешифрования с использованием шифра Виженера.
    """
    text = text.upper()
    key = key.upper()
    result = []
    key_length = len(key)
    for i, char in enumerate(text):
        if char in ALPHABET:
            shift = ALPHABET.index(key[i % key_length])
            if not encrypt:
                shift = -shift
            result.append(ALPHABET[(ALPHABET.index(char) + shift) % len(ALPHABET)])
        else:
            result.append(char)
    return ''.join(result)

def caesar_cipher(text, shift, encrypt=True):
    """
    Функция шифрования/дешифрования с использованием шифра Цезаря.
    """
    shift = int(shift)
    if not encrypt:
        shift = -shift
    result = []
    for char in text:
        if char in ALPHABET:
            new_index = (ALPHABET.index(char) + shift) % len(ALPHABET)
            result.append(ALPHABET[new_index])
        else:
            result.append(char)
    return ''.join(result)

def find_user(login):
    """
    Найти пользователя по логину.
    """
    return next((user for user in users if user['login'] == login), None)

def find_method(method_id):
    """
    Найти метод по его ID.
    """
    return next((method for method in methods if method['id'] == method_id), None)

def find_session(session_id):
    """
    Найти сессию по ее ID.
    """
    return next((session for session in sessions if session['id'] == session_id), None)

# Ресурсы API

class UserResource(Resource):
    def post(self):
        """
        Создать нового пользователя.
        """
        data = request.get_json()
        login = data.get('login').upper()
        secret = data.get('secret')
        if not (3 <= len(login) <= 10 и 3 <= len(secret) <= 10):
            return {"message": "Логин и секрет должны быть от 3 до 10 символов"}, 400
        if find_user(login):
            return {"message": "Пользователь уже существует"}, 400
        user = {'login': login, 'secret': secret}
        users.append(user)
        return {"message": "Пользователь успешно создан"}, 201

    def get(self):
        """
        Получить список всех пользователей.
        """
        return [{'login': user['login']} for user in users], 200

class MethodResource(Resource):
    def get(self):
        """
        Получить список всех методов.
        """
        return methods, 200

class SessionResource(Resource):
    def post(self):
        """
        Создать новую сессию для шифрования/дешифрования.
        """
        data = request.get_json()
        user_login = data.get('user_login').upper()
        user = find_user(user_login)
        if not user или user['secret'] != data.get('secret'):
            return {"message": "Неверный логин пользователя или секрет"}, 400
        
        method_id = data.get('method_id')
        method = find_method(method_id)
        if not method:
            return {"message": "Неверный ID метода"}, 400
        
        text = data.get('text', '').upper()
        params = data.get('params', {})
        action = data.get('action', 'encrypt')
        
        if action not in ['encrypt', 'decrypt']:
            return {"message": "Неверное действие. Должно быть 'encrypt' или 'decrypt'"}, 400
        
        start_time = time.time()
        if method_id == 1:
            key = params.get('key', '').upper()
            if not key:
                return {"message": "Параметр 'key' обязателен для шифра Виженера"}, 400
            result_text = vigenere_cipher(text, key, encrypt=(action == 'encrypt'))
        elif method_id == 2:
            shift = params.get('shift', 0)
            result_text = caesar_cipher(text, shift, encrypt=(action == 'encrypt'))
        else:
            return {"message": "Неизвестный метод"}, 400
        
        end_time = time.time()
        session = {
            'id': len(sessions) + 1,
            'user_id': user['login'],
            'method_id': method_id,
            'data_in': text,
            'params': params,
            'data_out': result_text,
            'status': 'completed',
            'created_at': datetime.now().isoformat(),
            'time_op': end_time - start_time
        }
        sessions.append(session)
        return session, 201

    def get(self, session_id):
        """
        Получить сессию по ее ID.
        """
        session = find_session(session_id)
        if not session:
            return {"message": "Сессия не найдена"}, 404
        return session, 200

    def delete(self, session_id):
        """
        Удалить сессию по ее ID.
        """
        data = request.get_json()
        secret = data.get('secret')
        session = find_session(session_id)
        if not session:
            return {"message": "Сессия не найдена"}, 404
        
        user = find_user(session['user_id'])
        if user['secret'] != secret:
            return {"message": "Неверный секрет"}, 400
        
        sessions.remove(session)
        return {"message": "Сессия удалена"}, 200

class AllSessionsResource(Resource):
    def get(self):
        """
        Получить список всех сессий.
        """
        return sessions, 200

# Инициализация методов
methods.append({
    'id': 1,
    'caption': 'Vigenere Cipher',
    'json_params': {'key': 'string'},
    'description': 'Метод шифрования алфавитного текста с использованием ряда различных шифров Цезаря на основе букв ключевого слова.'
})
methods.append({
    'id': 2,
    'caption': 'Caesar Cipher',
    'json_params': {'shift': 'int'},
    'description': 'Метод подстановочного шифра, где каждая буква в открытом тексте сдвигается на определенное количество позиций вниз по алфавиту.'
})

# Конечные точки API
api.add_resource(UserResource, '/users')
api.add_resource(MethodResource, '/methods')
api.add_resource(SessionResource, '/sessions', '/sessions/<int:session_id>')
api.add_resource(AllSessionsResource, '/sessions/all')

if __name__ == '__main__':
    app.run(debug=True)
