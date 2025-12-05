import pytest

from server import app

def test_showSummary_with_valid_email(client):
    """Test showSummary avec un email valide existant dans clubs.json"""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'john@simplylift.co' in response.data


def test_showSummary_with_unknown_email(client):
    """Test showSummary avec un email qui n'existe pas dans clubs.json"""
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 200
    assert b"Email not found, please try again" in response.data



def test_showSummary_with_empty_email(client):
    """Test showSummary avec un email vide"""
    response = client.post('/showSummary', data={'email': ''})
    assert response.status_code == 200
    assert b"Email not found, please try again" in response.data
