import pytest
import server


@pytest.fixture
def client():
    """
    Flask client fixture for testing the Flask application.
    Provides a test client for the Flask application defined in server.py.
    """
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs():
    """Données de test pour les clubs"""
    return [
        {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '24'},
        {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
        {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}
    ]


@pytest.fixture
def mock_competitions():
    """Données de test pour les compétitions"""
    return [
        {'name': 'Spring Festival', 'date': '2026-03-27 10:00:00', 'numberOfPlaces': '25'},
        {'name': 'Fall Classic', 'date': '2026-10-22 13:30:00', 'numberOfPlaces': '10'},
        {'name': 'Christmas Cup', 'date': '2024-12-22 13:30:00', 'numberOfPlaces': '2'}
    ]


@pytest.fixture(autouse=True)
def setup_mock_data(mock_clubs, mock_competitions):
    """Fixture qui configure les données mockées avant chaque test"""
    server.clubs = mock_clubs.copy()
    server.competitions = mock_competitions.copy()    
    yield
