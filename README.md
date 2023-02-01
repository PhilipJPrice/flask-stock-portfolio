# Flask-Stock-Portfolio
Flask Stock Portfolio Tutorial - TestDriven.io

-------------------------------------------
Current File Structure
-------------------------------------------

```
--app.py (Application Factory)
--config.py (Configuration for Application)
--instance (Stores run-time data, database)
--migrations (Database Migrations)
----versions (Database Version Control)
--project (Project Folder)
----static (CSS Files)
----users (About Page, 403 Page, Routing, Registration)
----templates (base.html, 404 Page, 405 Page)
----stocks (Stocks Page, Routing)
----models.py (DB Tables)
--requirements.txt (Pip Libraries)
--venv
--tests (Unit and Functional Tests)
```

-------------------------------------------
Commands for Mac (terminal) or Unix (shell)
-------------------------------------------

## Flask Commands

### Flask Help

```
flask --help
```

### Flask Version

```
flask --version
```

## Flask Development Server

```
flask --app app --debug run
```

## Virtual Environment
    
### Create Virtual Environment

```
python -m venv venv
```

### Activate Virtual Environment

```
source venv/bin/activate
```

## Pip Commands

### To Save Dependencies in txt File

```
pip freeze > requirements.txt
```

### To Install Dependencies

```
pip install -r requirements.txt
```

## Tests with Pytest

### All Tests

```
python -m pytest
```

### Unit Tests

```
python -m pytest tests/unit
```

### Functional Tests

```
python -m pytest tests/functional
```

### Call Structure of Fixtures with Pytest

```
python -m pytest --setup-show
```

### Coverage (pytest-cov) Library

```
python -m pytest --cov=project
```

### Database Tests

```
python -m pytest -v tests/unit/test_models.py
```

## Routes

### Flask Routes Command

```
flask routes
```

### Flask Shell - Routes and Blueprints

```
flask shell
```

```
print(app.url_map)
```

```
print(app.blueprints)
```

```
quit()
```

## Secret Keys

### Python 3.6 or higher

```
python
```

```
import secrets
```

```
print(secrets.token_bytes(32))
```

### Python earlier than 3.6

```
python
```

```
import os
```

```
print(os.urandom(32))
```

## SQLite Database

### Create (Manually)

```
flask shell
```

```
from project import database
```

```
database.create_all()
```

```
quit()
```

### Create (Using Flask-Migrate)

```
flask db init
```

```
flask db migrate -m "add tableName table"
```

```
flask db upgrade
```

### Resetting Database

```
flask shell
```

```
from project import database
```

```
database.drop_all()
```

```
database.create_all()
```

```
quit()
```

### Troubleshooting and Steps Before Deployment

```
1. Delete SQLite database file (instance/app.db)
2. Delete "__pycache__" folders in top-level and "project" directory
3. Delete "migrations" directory
4. Run "Create (Using Flask-Migrate)" Procedure
```

## Flask Shell

```
flask shell
```

### Print App Attributes in Flask Shell

```
print(dir(app))
```

### Quit Flask Shell

```
quit()
```

## Flask CLI Commands

```
flask stocks --help
```

```
flask stocks <command>
```

### Stocks Blueprint Commands

```
flask stocks create_default_set
```

```
flask stocks create '<SYMB>' '<##>' '<$$.$$>'
```

```
flask stocks create 'SBUX' '25' '123.45'
```

## Email Configuration

### Test Function (tests/functional/test_users.py, test_valid_registration())

```
assert outbox[0].sender == 'email@email.com'
```

### Environment Variables

```
export MAIL_USERNAME=<insert_email_address_here>
```

```
export MAIL_PASSWORD=<insert_password_here>
```

## Creating a Form

```
Create a new:
```

```
    1. Class that defines the form (projects/users/forms.py)
```

```
    2. Route for displaying the form and processing the data from the form (projects/users/route.py)
```

```
    3. Template for displaying the form (projects/users/templates/users/fileName.html)
```

## Login

### Fresh Login (Flask-Login Package)

[Flask-Login Docs](https://flask-login.readthedocs.io/en/latest/#fresh-logins)
