import json
import pytest
import server

TEST_CLUBS = [
    {'name': 'Club Example 1', 'email': 'club1@example.com', 'points': '24'},
    {'name': 'Club Example 2', 'email': 'club2@example.com', 'points': '4'},
    {'name': 'Club Example 3', 'email': 'club3@example.com', 'points': '12'}
]

TEST_COMPETITIONS = [
    {'name': 'Competition Example 1', 'date': '2026-03-27 10:00:00', 'numberOfPlaces': '25'},
    {'name': 'Competition Example 2', 'date': '2026-10-22 13:30:00', 'numberOfPlaces': '10'},
    {'name': 'Competition Example 3', 'date': '2024-12-22 13:30:00', 'numberOfPlaces': '2'}
]

@pytest.fixture
def client():
    """
    Fixture Flask client pour tester l'application Flask.
    Fournit un client de test pour l'application définie dans server.py.
    """
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def temp_json_files(tmp_path, monkeypatch):
    """
    Fixture qui crée des fichiers JSON temporaires pour les tests d'intégration.
    Modifie les chemins des fichiers dans server.py pour utiliser les fichiers temporaires.
    """
    clubs_file = tmp_path / "clubs.json"
    competitions_file = tmp_path / "competitions.json"
    
    initial_clubs = {"clubs": TEST_CLUBS}  
    initial_competitions = {"competitions": TEST_COMPETITIONS}
    
    with open(clubs_file, 'w') as f:
        json.dump(initial_clubs, f, indent=4) 
    with open(competitions_file, 'w') as f:
        json.dump(initial_competitions, f, indent=4)
    
    def loadClubs_temp():
        with open(clubs_file) as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs
    
    def loadCompetitions_temp():
        with open(competitions_file) as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
    
    def updateClubs_temp(clubs):
        with open(clubs_file, 'w') as c:
            json.dump({'clubs': clubs}, c, indent=4)
    
    def updateCompetitions_temp(competitions):
        with open(competitions_file, 'w') as comps:
            json.dump({'competitions': competitions}, comps, indent=4)
    
    monkeypatch.setattr(server, 'loadClubs', loadClubs_temp)
    monkeypatch.setattr(server, 'loadCompetitions', loadCompetitions_temp)
    monkeypatch.setattr(server, 'updateClubs', updateClubs_temp)
    monkeypatch.setattr(server, 'updateCompetitions', updateCompetitions_temp)
    
    server.clubs = loadClubs_temp()
    server.competitions = loadCompetitions_temp()
    
    yield {
        'clubs_file': clubs_file,
        'competitions_file': competitions_file
    }
