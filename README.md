## Запуск с Docker Compose

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/hellsinger1337/textgen-django.git
   ```
2. Перейдите в директорию:
    ```bash
    cd textgen-django
    ```
3. Создайте файл .env на основе .env.example и заполните нужные переменные
4. Запустите:
    ```bash
    docker-compose up --build
    ```
5. Приложение будет доступно на http://localhost:8000/api/(или другой порт, если вы его изменили)
