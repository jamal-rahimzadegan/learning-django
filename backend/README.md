# Social Event Management

A simple Django project for managing social events. This application demonstrates a multi-database setup where the core Django application uses a default database, while the `events` application connects to a separate, pre-existing database.

## Features

- Create, view, and list social events.
- Associates events with organizers (users).
- Demonstrates routing database queries for a specific app to an external database.

## Project Structure

- ``: The main Django project directory.
- `events/`: The Django app for managing events.
- `templates/`: Contains the HTML templates.
- `static/`: Contains static files (CSS, JS, images).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd social-event
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    You will need to install Django and a PostgreSQL adapter.
    ```bash
    pip install Django psycopg2-binary
    ```

4.  **Database Setup:**
    This project requires two PostgreSQL databases.
    - Create a database named `django_admin_db` for Django's internal use (auth, admin, etc.).
    - Create a second database named `social_event`. This database must contain pre-existing `users` and `events` tables that match the schemas in `events/models.py`.
    - Update the database credentials in `backend/settings/base.py` to match your local setup.

5.  **Run Migrations:**
    Run migrations to set up the tables in your `default` (`django_admin_db`) database. The router configuration will prevent migrations from running on the `social_event` database.
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/events/`.