# Comments

## Comments Project

![Alt text](fsLr4EV07s.gif)

### Features

- **Uses JWT for Authentication:** Secure user authentication with JSON Web Tokens.
- **Commenting System:** Allows users to leave comments or replies.
- **File Attachments:** Provides the ability to attach files to comments (images, text files). File size limit for `.txt` files is 100KB.
- **File Management:** View and download attached files.
- **Comment Preview:** Allows users to preview their comments before posting.
- **Root Comments Display:** Displays root comments in a table format.
- **Like System:** Includes a system for liking comments.

### Dependencies

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

### Installation and Configuration

#### Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/adamant-antithesis-work/comments.git

2. **Navigate to the Project Directory:**
   ```bash
	cd comments_project

3. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
	python -m venv env
   
4. **Activate the Virtual Environment:**
   ```bash
	On Windows: env\Scripts\activate
	On macOS and Linux: source env/bin/activate

6. **Install Dependencies:**
   ```bash
	pip install -r requirements.txt

7. **Create the Database:**
   ```bash
	Access the PostgreSQL shell with:

	psql -U <username>  # Default username is 'postgres', password is 'postgres'
	
	In the PostgreSQL shell, create the database:

	CREATE DATABASE comments_db;

8. **Exit the PostgreSQL Shell:**
   ```bash
	\q

9. **Create a .env File:**

   **To generate your SECRET_KEY, use:**
   
   	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   
   **.env File Content:**
   
	   SECRET_KEY="Your_Secret_Key"
	   DATABASE_URL=postgres://postgres:postgres@db:5432/comments_db
	   DJANGO_DB_NAME=comments_db
	   DJANGO_DB_USER="Your_DB_Username"
	   DJANGO_DB_PASSWORD="Your_DB_Password"
	   DJANGO_DB_HOST=db
	   DJANGO_DB_PORT=5432

10. **Update Database Settings in settings.py:**

   **Uncomment and configure the database settings:**

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

11. **Uncomment the line:**
   
		# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

12. **Comment the line:**

		STATIC_ROOT = os.path.join(BASE_DIR, 'static')	

13. **Create and Apply Migrations:**

        python manage.py makemigrations
	     python manage.py migrate

14. **Load Initial Data:**

	      python manage.py loaddata comments/fixtures/initial_data.json
    
15. **Start the Server:**

	      python manage.py runserver

--Running with Docker Compose:

1. **Create a .env File:**

*** To generate your SECRET_KEY, use:

	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
 
*** **.env File Content:**

	SECRET_KEY="Your_Secret_Key"
	DATABASE_URL=postgres://postgres:postgres@db:5432/comments_db
	DJANGO_DB_NAME=comments_db
	DJANGO_DB_USER="Your_DB_Username"
	DJANGO_DB_PASSWORD="Your_DB_Password"
	DJANGO_DB_HOST=db
	DJANGO_DB_PORT=5432

2. **Run Docker Compose:**

	   docker-compose up --build

	   If the server does not start, try:

	   docker-compose up

3. **Enter the Django container:**

           docker exec -it django_backend /bin/bash
   
4. **Load Initial Data:**

	      python manage.py loaddata comments/fixtures/initial_data.json
