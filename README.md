# Book Store E-commerce Application

This repository contains the source code and configuration instructions for the Book Store E-commerce Application. It is a web-based platform developed using Python Django, PostgreSQL, Django Celery, and Redis server. The application provides a seamless shopping experience for users, allowing them to browse and purchase books online. This README file will guide you through the setup and configuration process.

## Requirements

Before setting up the application, make sure you have the following requirements installed:

- Python 3.6+
- Django 3.2 web framework
- PostgreSQL
- Django Celery
- Redis server

## Setup and Configuration

Please follow the steps below to set up and configure the application:

1. Create a virtual environment using the following command:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - For Linux:
     ```
     source ./venv/bin/activate
     ```
   - For Windows:
     ```
     .\venv\Scripts\activate
     ```

3. Install all dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

4. Perform database migration using Django's migrate command:
   ```
   python manage.py migrate
   ```

5. Start the Redis server:
   - For Linux:
     ```
     redis-server
     ```
   - For Windows, refer to the Redis documentation for installation and startup instructions.

   Note: By default, Redis server listens on port 6379. If your Redis server uses a different port, update the configuration in the `settings.py` file.

6. Create a `.env` file based on the provided `.env.example` file. Fill in the required information for the following settings:
   ```
   ENGINE=django.db.backends.postgresql
   NAME=db-name
   USER=username
   PASSWORD=password
   HOST=localhost
   PORT=5432

   # EMAIL Settings
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=''
   EMAIL_HOST_PASSWORD='**************'
   EMAIL_USE_TLS=True
   ```

7. Create a superuser to access the admin interface:
   ```
   python manage.py createsuperuser
   ```

8. Run the default setup command to populate initial values:
   ```
   python manage.py configure_default
   ```

## Running the Application

To run the application, use the following command:
```
python manage.py runserver
```

You can now access the Book Store E-commerce Application by opening your web browser and navigating to `http://localhost:8000`.

## Contributing

If you would like to contribute to the development of this application, please follow the guidelines outlined in the CONTRIBUTING.md file.

## License

This project is licensed under the MIT License.