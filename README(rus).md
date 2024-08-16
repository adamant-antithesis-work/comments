# Comments

## Comments Project

### Фичи

- **Используется JWT:** Secure user authentication with JSON Web Tokens.
- **Позволяет оставить комментарий(или ответ на комментарий):** Allows users to leave comments or replies.
- **Прикрепление файлов:** Provides the ability to attach files to comments (images, text files). File size limit for `.txt` files is 100KB.
- **Доступен просмотр и скачивание прикреплённых файлов:** View and download attached files.
- **CДоступен предпросмотр комментария:** Allows users to preview their comments before posting.
- **Отображение корневых комментариев в виде таблицы:** Displays root comments in a table format.
- **Система лайков:** Includes a system for liking comments.

### Зависимости

- `asgiref==3.8.1`
- `captcha==0.6.0`
- `Django==5.0.8`
- `django-ranged-response==0.2.0`
- `djangorestframework==3.15.2`
- `djangorestframework-simplejwt==5.3.1`
- `pillow==10.4.0`
- `psycopg2-binary==2.9.9`
- `PyJWT==2.9.0`
- `python-decouple==3.8`
- `python-dotenv==1.0.1`
- `sqlparse==0.5.1`
- `tzdata==2024.1`

### Установка и конфигурация (доступны варианты локального запуска и Docker Compose)

#### Локальный запуск

1. **Склонируйте репозиторий командой:**
   ```bash
   git clone https://github.com/adamant-antithesis-work/comments.git

2. **Перейдите в каталог на уровень с файлом manage.py:**
   ```bash
	cd comments_project

3. **Создайте виртуальное окружение командой(опционально, но предпочтительно):**
   ```bash
	python -m venv env
   
4. **Активируйте виртуальное окружение:**
   ```bash
	On Windows: env\Scripts\activate
	On macOS and Linux: source env/bin/activate

5. **Установите зависимости командой(если команда недоступна перейдите в каталог на уровень выше)::**
   ```bash
	pip install -r requirements.txt

6. **Создайте базу данных с названием "comments_db":**
   ```bash
	Access the PostgreSQL shell with:

	psql -U <username>  # Default username is 'postgres', password is 'postgres'
	
	In the PostgreSQL shell, create the database:

	CREATE DATABASE comments_db;

7. **Выходите из PostgreSQL shell(введите команду \q и нажмите Enter):**
   ```bash
	\q

8. **Создайте файл ".env" на уровне с файлами докер:**

   **Что бы сгенерировать секретный ключ можете использовать команду:**
   
       python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   
   **.env File Content:**
   
	   	SECRET_KEY="Your_Secret_Key"
	   	DATABASE_URL=postgres://postgres:postgres@db:5432/comments_db
	   	DJANGO_DB_NAME=comments_db
	   	DJANGO_DB_USER="Your_DB_Username"
	   	DJANGO_DB_PASSWORD="Your_DB_Password"
	   	DJANGO_DB_HOST=db
	   	DJANGO_DB_PORT=5432

9. **Введите данные для подключения к базе данных в файле "settings.py"**

10. **Расскоментируйте участок кода и введите данные для подключения к базе данных в файле "settings.py"**

		DATABASES = {
		    'default': {
		        'ENGINE': 'django.db.backends.postgresql',
		        'NAME': 'comments_db',
		        'USER': 'Your_DB_Username',
		        'PASSWORD': 'Your_DB_Password',
		        'HOST': 'localhost',
		        'PORT': '5432',
		    }
		}

11. **Расскомментируйте строчку:**
   
		# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

12. **Закомментируйте строчку:**

		STATIC_ROOT = os.path.join(BASE_DIR, 'static')	

13. **Создайте и примените миграции (проверьте что находитесь в каталоге на уровне с файлом manage.py) с помощью этих команд:**

        python manage.py makemigrations
	     python manage.py migrate

14. **Добавьте фикстуру с помощь команды:**

	      python manage.py loaddata comments/fixtures/initial_data.json
    
15. **Теперь можете запускать сервер с помощью команды:**

	      python manage.py runserver

--Запуск с помощью Docker Compose:

1. **Создайте файл ".env" на уровне с файлами докер:**

*** Что бы сгенерировать секретный ключ можете использовать команду: 

	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
 
*** **.env File Content:**

	SECRET_KEY="Your_Secret_Key"
	DATABASE_URL=postgres://postgres:postgres@db:5432/comments_db
	DJANGO_DB_NAME=comments_db
	DJANGO_DB_USER="Your_DB_Username"
	DJANGO_DB_PASSWORD="Your_DB_Password"
	DJANGO_DB_HOST=db
	DJANGO_DB_PORT=5432

2. **Находясь на уровне с файлом docker-compose введите команду:**

       docker-compose up --build

       Если по какой-то причине сервер после этого не стартовал ввести команду:

       docker-compose up

3. **Войдите в контейнер Django:**

        docker exec -it django_backend /bin/bash
   
3. **Загрузите исходные данные:**

       python manage.py loaddata comments/fixtures/initial_data.json
