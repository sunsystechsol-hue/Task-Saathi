# TaskSaathi Project Setup Guide

This repository contains both the frontend and backend components of the TaskSaathi application.

## Project Structure

- `frontend/` - HTML/CSS/JavaScript frontend
- `django-boilerplate/` - Django backend API

## Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js (optional, for frontend development)

## Backend Setup (Django)

1. Navigate to the Django project directory:
   ```
   cd django-boilerplate
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Database Configuration:
   - The project is configured to use PostgreSQL
   - Make sure PostgreSQL is installed and running
   - Update database settings in `src/vault.py` if needed (currently set to use localhost)

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the Django development server:
   ```
   python manage.py runserver
   ```
   The backend will be available at http://localhost:8000/

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Start a simple HTTP server:
   ```
   python -m http.server 8080
   ```
   The frontend will be available at http://localhost:8080/

3. Open the application in your browser:
   - Login page: http://localhost:8080/login.html
   - Signup page: http://localhost:8080/signup.html

## API Endpoints

- Login: `http://localhost:8000/login/`
- Register: `http://localhost:8000/register/`
- Tasks: `http://localhost:8000/tasks/`

## Troubleshooting

- **Database Connection Issues**: Ensure PostgreSQL is running and the connection settings in `src/vault.py` are correct
- **404 Errors**: Check that API endpoints in `frontend/js/api.js` match the backend URL patterns
- **Registration Errors**: Ensure the RegisterUserView in the backend is properly handling new user registrations

## Development Workflow

1. Start both the frontend and backend servers
2. Make changes to the code
3. Test your changes in the browser
4. Commit your changes when ready

## Additional Resources

For more detailed information, refer to:
- Django documentation: https://docs.djangoproject.com/
- Project-specific documentation in the `docs/` directory