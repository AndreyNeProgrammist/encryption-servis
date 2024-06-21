# encryption-servis

## Описание

Это REST API сервис для шифрования данных с использованием методов Виженера и сдвига.

## Установка и запуск

1. Клонируйте репозиторий:

   git clone https://github.com/AndreyNeProgrammist/encryption-servis.git
    cd encryption-servis

2. Установите зависимости:
  
    pip install flask flask-restful

3. Запустите приложение:
  
    python main.py
  

## Использование

### Добавить пользователя

POST /users

### Посмотреть список пользователей (без секретов)

GET /users

### Просмотреть медоты шифрования 

GET /methods

### Зашифровать/расшифровать данные выбранным методом

POSt /sessions

### Получить данные по сеансу шифрования

GET /sessions/№

### Получить данные по всем сеансам шифрования 

GET /sessions/all

### Удалить сеанс шифрования 

DELETE /sessions/№




