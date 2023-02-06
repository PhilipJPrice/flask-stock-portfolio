"""
This file (test_models.py) conatins the unit tests for the models.py file.
"""
from project.models import Stock

def test_new_stock(new_stock):
    """
    GIVEN a Stock model
    WHEN a new Stock object is created
    THEN check the symbol, number of shares, and purchase price fields are defined correctly
    """
    assert new_stock.stock_symbol == 'IBM'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678
    assert new_stock.user_id == 17
    assert new_stock.purchase_date.year == 2023
    assert new_stock.purchase_date.month == 2
    assert new_stock.purchase_date.day == 3

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User object is created
    THEN check the email is valid and hashed password does not equal the password provided
    """

    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsAwesome123'

def test_set_password(new_user):
    """
    GIVEN a User model
    WHEN the user's password is changed
    THEN check the password has been changed
    """
    new_user.set_password('FlaskIsStillAwesome456')
    assert new_user.email == 'patrick@email.com'
    assert new_user.password_hashed != 'FlaskIsStillAwesome456'
    assert new_user.is_password_correct('FlaskIsStillAwesome456')

from datetime import datetime

def test_get_stock_data_success(new_stock, mock_requests_get_success_daily):
    """
    GIVEN a Flask application configured for testing and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check that the stock data is updated
    """
    new_stock.get_stock_data()
    assert new_stock.stock_symbol == 'IBM'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678 # $406.78 -> integer
    assert new_stock.purchase_date.date() == datetime(2023, 2, 3).date()
    assert new_stock.current_price == 13694 # $136.94 -> integer
    assert new_stock.current_price_date.date() == datetime.now().date()
    assert new_stock.position_value == (13694*16)

def test_get_stock_data_api_rate_limit_exceeded(new_stock, mock_requests_get_api_rate_limit_exceeded):
    """
    GIVEN a Flask application configured for testing and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful but the API rate limit is exceeded
    THEN check that the stock data is not updated
    """
    new_stock.get_stock_data()
    assert new_stock.stock_symbol == 'IBM'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_date.date() == datetime(2023, 2, 3).date()
    assert new_stock.current_price == 0
    assert new_stock.current_price_date is None
    assert new_stock.position_value == 0

def test_get_stock_data_failure(new_stock, mock_requests_get_failure):
    """
    GIVEN a Flask application configured for testing and a monkeypatche version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check that the stock data is not updated
    """
    new_stock.get_stock_data()
    assert new_stock.stock_symbol == 'IBM'
    assert new_stock.number_of_shares == 16
    assert new_stock.purchase_price == 40678 # $406.78 -> integer
    assert new_stock.purchase_date.date() == datetime(2023, 2, 3).date()
    assert new_stock.current_price == 0
    assert new_stock.current_price_date is None
    assert new_stock.position_value == 0

def test_get_stock_data_success_two_calls(new_stock, mock_requests_get_success_daily):
    """
    GIVEN a Flask application configured for testing and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check that the stock data is updated
    """
    assert new_stock.stock_symbol == 'IBM'
    assert new_stock.current_price == 0
    assert new_stock.current_price_date is None
    assert new_stock.position_value == 0
    new_stock.get_stock_data()
    assert new_stock.current_price == 13694 # $136.94 -> integer
    assert new_stock.current_price_date.date() == datetime.now().date()
    assert new_stock.position_value == (13694*16)
    new_stock.get_stock_data()
    assert new_stock.current_price == 13694 # $136.94 -> integer
    assert new_stock.current_price_date.date() == datetime.now().date()
    assert new_stock.position_value == (13694*16)

from freezegun import freeze_time

@freeze_time('2023-02-03')
def test_get_weekly_stock_data_success(new_stock, mock_requests_get_success_weekly):
    """
    GIVEN a Flask application configured for testing and a monkeypatchedd version of requests.get()
    WHEN the HTTP response is set to successful
    THEN check the HTTP response
    """
    title, labels, values = new_stock.get_weekly_stock_data()
    assert title == 'Weekly Prices (IBM)'
    assert len(labels) == 4
    assert labels[0].date() == datetime(2023, 1, 13).date()
    assert labels[1].date() == datetime(2023, 1, 20).date()
    assert labels[2].date() == datetime(2023, 1, 27).date()
    assert len(values) == 4
    assert values[0] == '145.8900'
    assert values[1] == '141.2000'
    assert values[2] == '134.3900'
    assert datetime.now() == datetime(2023, 2, 3)

def test_get_weekly_stock_data_failure(new_stock, mock_requests_get_failure):
    """
    GIVEN a Flask application configured for testing and a monkeypatched version of requests.get()
    WHEN the HTTP response is set to failed
    THEN check the HTTP response
    """
    title, labels, values = new_stock.get_weekly_stock_data()
    assert title == 'Stock chart is unavailable.'
    assert len(labels) == 0
    assert len(values) == 0
