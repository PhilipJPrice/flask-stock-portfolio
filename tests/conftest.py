import pytest
from project import create_app
from flask import current_app
from project import database

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')
    flask_app.extensions['mail'].suppress = True

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with flask_app.app_context():
            flask_app.logger.info('Creating database tables in test_client fixture...')

            # Create the database and the database table(s)
            database.create_all()

        yield testing_client # this is where testing happens

        with flask_app.app_context():
            database.drop_all()

#################
##### USERS #####
#################
from project.models import User

@pytest.fixture(scope='module')
def new_user():
    user = User('patrick@email.com', 'FlaskIsAwesome123')
    return user

@pytest.fixture(scope='module')
def register_default_user(test_client):
    # Register the default user
    test_client.post('/users/register',
                    data={'email': 'patrick@gmail.com',
                        'password': 'FlaskIsAwesome123'},
                    follow_redirects=True)
    return

@pytest.fixture(scope='function')
def log_in_default_user(test_client, register_default_user):
    # Log in the default user
    test_client.post('/users/login',
                    data={'email': 'patrick@gmail.com',
                            'password': 'FlaskIsAwesome123'},
                    follow_redirects=True)

    yield # this is where testing happens!

    # Log out the default user
    test_client.get('/users/logout', follow_redirects=True)

@pytest.fixture(scope='module')
def register_second_user(test_client):
    """Registers the second user using the '/users/register' route."""
    test_client.post('/users/register',
                     data={'email': 'patrick@yahoo.com',
                           'password': 'FlaskIsTheBest987'})

@pytest.fixture(scope='function')
def log_in_second_user(test_client, register_second_user):
    # Log in the user
    test_client.post('/users/login',
                     data={'email': 'patrick@yahoo.com',
                           'password': 'FlaskIsTheBest987'})

    yield # this is where the testing happens!

    # Log out the user
    test_client.get('/users/logout', follow_redirects=True)

####################
##### DATABASE #####
####################
from project.models import Stock

@pytest.fixture(scope='function')
def new_stock():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')
    flask_app.extensions['mail'].suppress = True

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with flask_app.app_context():
            stock = Stock('IBM', '16', '406.78', 17, datetime(2023, 2, 3))
            yield stock # this is where testing happens!

##########################
##### PASSWORD RESET #####
##########################
from datetime import datetime

@pytest.fixture(scope='function')
def confirm_email_default_user(test_client, log_in_default_user):
    # Mark the user as having their email address confirmed
    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.email_confirmed = True
    user.email_confirmed_on = datetime(2023, 1, 29)
    database.session.add(user)
    database.session.commit()

    yield user

    # Mark the user as not having their email address confirmed (clean up)
    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.email_confirmed = False
    user.email_confirmed_on = None
    database.session.add(user)
    database.session.commit()

@pytest.fixture(scope='function')
def afterwards_reset_default_user_password():
    yield # this is where testing happens

    # Since a test using this fixture could change the password for the default user,
    # reset the password back to the default password
    user = User.query.filter_by(email='patrick@gmail.com').first()
    user.set_password('FlaskIsAwesome123')
    database.session.add(user)
    database.session.commit()

@pytest.fixture(scope='function')
def add_stocks_for_default_user(test_client, log_in_default_user):
    # Add three stocks for the default user
    test_client.post('/add_stock', data={'stock_symbol': 'SAM',
                                        'number_of_shares': '27',
                                        'purchase_price': '301.23',
                                        'purchase_date': '2020-07-01'})
    test_client.post('/add_stock', data={'stock_symbol': 'COST',
                                        'number_of_shares': '76',
                                        'purchase_price': '14.67',
                                        'purchase_date': '2019-05-26'})
    test_client.post('/add_stock', data={'stock_symbol': 'TWTR',
                                        'number_of_shares': '146',
                                        'purchase_price': '34.56',
                                        'purchase_date': '2020-02-03'})
    return

##################
###### API #######
##################

import requests

# --------------
# Helper Classes
# --------------

class MockSuccessResponseDaily(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url

    def json(self):
        return {
            'Meta Data': {
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2023-02-03"
        },
        'Time Series (Daily)': {
            "2023-02-03": {
                "4. close": "136.94",
            },
            "2023-02-02": {
                "4. close": "136.39",
            }
        }
    }

class MockApiRateLimitExceededResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url

    def json(self):
        return {
            'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is ' + '5 calls per minute and 500 calls per day.'
        }

class MockFailedResponse(object):
    def __init__(self, url):
        self.status_code = 404
        self.url = url

    def json(self):
        return {'error': 'bad'}

class MockSuccessResponseWeekly(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url

    def json(self):
        return {
            'Meta Data': {
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2023-02-03",
        },
        'Weekly Adjusted Time Series': {
            "2023-02-03": {
                "4. close": "136.9400",
            },
            "2023-01-27": {
                "4. close": "134.3900",
            },
            "2023-01-20": {
                "4. close": "141.2000",
            },
            "2023-01-13": {
                "4. close": "145.8900",
            }
        }
    }
@pytest.fixture(scope='function')
def mock_requests_get_success_daily(monkeypatch):
    # Create a mock for the requests.get() call to prevent making the actual API call
    def mock_get(url):
        return MockSuccessResponseDaily(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)

@pytest.fixture(scope='function')
def mock_requests_get_api_rate_limit_exceeded(monkeypatch):
    def mock_get(url):
        return MockApiRateLimitExceededResponse(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)

@pytest.fixture(scope='function')
def mock_requests_get_failure(monkeypatch):
    def mock_get(url):
        return MockFailedResponse(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)

@pytest.fixture(scope='function')
def mock_requests_get_success_weekly(monkeypatch):
    # Create a mock for the requests.get() call to prevent making the actual API call
    def mock_get(url):
        return MockSuccessResponseWeekly(url)

    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo'
    monkeypatch.setattr(requests, 'get', mock_get)
