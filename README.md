# Flask-Stock-Portfolio
Flask Stock Portfolio Tutorial - TestDriven.io

-------------------------------------------
Current File Structure
-------------------------------------------

--app.py (Application Factory)
--config.py (Configuration for Application)
--instance (Stores run-time data)
--project (Project Folder)
----static (CSS Files)
----users (About Page HTML and Routing)
----templates (Base.html)
----stocks (Stocks HTML and Routing)
----__init__.py
----__pycache__
--requirements.txt (Pip Libraries)
--venv
--tests (Unit and Functional Tests)
--README.md
--flask-stock-portfolio.log (old)
--__pycache__

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

```
python -m pytest
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
