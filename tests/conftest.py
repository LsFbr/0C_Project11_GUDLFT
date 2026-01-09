import json
import pytest
import server

TEST_CLUBS = [
    {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '24'},
    {'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': '4'},
    {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk', 'points': '12'}
]

TEST_COMPETITIONS = [
    {'name': 'Spring Festival', 'date': '2026-03-27 10:00:00', 'numberOfPlaces': '25'},
    {'name': 'Fall Classic', 'date': '2026-10-22 13:30:00', 'numberOfPlaces': '10'},
    {'name': 'Christmas Cup', 'date': '2024-12-22 13:30:00', 'numberOfPlaces': '2'}
]


# FIXTURES COMMUNES

@pytest.fixture
def client():
    """
    Fixture Flask client pour tester l'application Flask.
    Fournit un client de test pour l'application définie dans server.py.
    """
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client


# FIXTURES POUR TESTS UNITAIRES

@pytest.fixture(autouse=True)
def setup_mock_data(request):
    """
    Fixture qui configure les données mockées avant chaque test unitaire.
    Désactivée automatiquement pour les tests d'intégration.
    """
    # Vérifier si on est dans un test d'intégration
    test_path = str(request.node.fspath)
    if 'integration' in test_path or '\\integration\\' in test_path or '/integration/' in test_path:
        yield
        return
    
    # Sinon, utiliser les données mockées
    server.clubs = TEST_CLUBS
    server.competitions = TEST_COMPETITIONS
    yield


# FIXTURES POUR TESTS D'INTÉGRATION

@pytest.fixture
def temp_json_files(tmp_path, monkeypatch):
    """
    Fixture qui crée des fichiers JSON temporaires pour les tests d'intégration.
    Modifie les chemins des fichiers dans server.py pour utiliser les fichiers temporaires.
    """
    # Créer les fichiers JSON temporaires avec les données initiales
    clubs_file = tmp_path / "clubs.json"
    competitions_file = tmp_path / "competitions.json"
    
    # Données initiales pour les clubs
    initial_clubs = {"clubs": TEST_CLUBS}
    
    # Données initiales pour les compétitions
    initial_competitions = {"competitions": TEST_COMPETITIONS}
    
    # Écrire les fichiers JSON temporaires
    with open(clubs_file, 'w') as f:
        json.dump(initial_clubs, f, indent=4)
    
    with open(competitions_file, 'w') as f:
        json.dump(initial_competitions, f, indent=4)
    
    # Modifier les fonctions pour utiliser les fichiers temporaires
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
    
    # Patcher les fonctions dans server.py
    monkeypatch.setattr(server, 'loadClubs', loadClubs_temp)
    monkeypatch.setattr(server, 'loadCompetitions', loadCompetitions_temp)
    monkeypatch.setattr(server, 'updateClubs', updateClubs_temp)
    monkeypatch.setattr(server, 'updateCompetitions', updateCompetitions_temp)
    
    # Recharger les données dans server.py
    server.clubs = loadClubs_temp()
    server.competitions = loadCompetitions_temp()
    
    yield {
        'clubs_file': clubs_file,
        'competitions_file': competitions_file
    }
