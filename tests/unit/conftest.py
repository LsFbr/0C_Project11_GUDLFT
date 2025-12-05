import pytest
from server import app

@pytest.fixture
def client():
    """
    Flask client fixture for testing the Flask application.
    Provides a test client for the Flask application defined in server.py.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client