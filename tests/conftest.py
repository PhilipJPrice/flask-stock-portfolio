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

####################
##### DATABASE #####
####################
from project.models import Stock

@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78', 17, datetime(2023, 2, 1))
    return stock

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
