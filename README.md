# Flask-Stock-Portfolio
Flask Stock Portfolio Tutorial - TestDriven.io

-------------------------------------------
Current File Structure
-------------------------------------------

```
--app.py (Application Factory)
--config.py (Configuration for Application)
--instance (Stores run-time data, Database)
--migrations (Database Migrations)
----versions (Database Version Control)
--project (Project Folder)
----static (CSS Files)
----users (About Page, 403 Page, Routing)
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
python -m pytest --setup-show [tests/function, tests/unit, --cov=project]
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

```
flask routes
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

## Creating SQLite Database

### Manually

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

### Using Flask-Migrate

```
flask db init
```

```
flask db migrate -m "add tableName table"
```

```
flask db upgrade
```

### Troubleshooting and Steps Before Deployment

```
1. Delete SQLite database file (instance/app.db)
2. Delete "__pycache__" folders in top-level and "project" directory
3. Delete "migrations" directory
4. Run Flask-Migrate Procedure
```
