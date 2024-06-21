# Flask Encryption Service

## Описание

Это REST API сервис для шифрования данных с использованием методов Виженера и сдвига.

## Установка и запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/yourusername/encryption-service.git
    cd encryption-service
    ```

2. Установите зависимости:
    ```bash
    pip install flask flask-restful
    ```

3. Запустите приложение:
    ```bash
    python app.py
    ```

## Использование

### Добавить пользователя

POST /users

```json
{
    "login": "username",
    "secret": "secretkey"
}