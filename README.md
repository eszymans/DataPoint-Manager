# DataPoint Manager

A Flask-based web application and REST API for managing data points consisting of weight, height, and category. The application provides a user-friendly HTML interface and a JSON API for CRUD (Create, Read, Delete) operations.

## Features

* **Web Interface**:
    * View all data points in a table.
    * Add new data points via a form.
    * Delete data points.
    * Responsive design using custom CSS.
* **REST API**:
    * Endpoints to fetch, add, and delete data programmatically.
* **Database**:
    * SQLAlchemy ORM for database interaction.
    * Flask-Migrate for handling database schema migrations.

## Project Structure

```text
app/
├── api/                # API Blueprint and routes
├── static/             # CSS files
├── templates/          # HTML templates (Jinja2)
├── web/                # Web Interface Blueprint and routes
├── __init__.py         # App factory and configuration
├── extensions.py       # DB and Migrate instances
└── models.py           # Database models
config.py               # Configuration file (required)
