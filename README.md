# Comments

## Comments Project

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
