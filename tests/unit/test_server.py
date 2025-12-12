import server

# showSummary tests
def test_showSummary_with_valid_email(client):
    """
    Test showSummary avec un email valide existant dans clubs.json
    Vérifie que la fonction showSummary retourne un code 200 et que le message de bienvenue et l'email sont présents dans la réponse.
    """
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'john@simplylift.co' in response.data


def test_showSummary_with_unknown_email(client):
    """
    Test showSummary avec un email qui n'existe pas dans clubs.json
    Vérifie que la fonction showSummary retourne un code 200 et que le message d'erreur est présent dans la réponse.
    """
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 200
    assert b"Email not found, please try again" in response.data


def test_showSummary_with_empty_email(client):
    """
    Test showSummary avec un email vide
    Vérifie que la fonction showSummary retourne un code 200 et que le message d'erreur est présent dans la réponse.
    """
    response = client.post('/showSummary', data={'email': ''})
    assert response.status_code == 200
    assert b"Email not found, please try again" in response.data

# purchasePlaces tests
def test_purchasePlaces_success(mocker, client):
    """
    Test purchasePlaces avec une réservation réussie
    Vérifie que la fonction purchasePlaces retourne un code 200 et que le message de succès est présent dans la réponse.
    Vérifie que les fonctions updateClubs et updateCompetitions sont appelées une fois.
    """
    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    mock_update_clubs.assert_called_once()
    mock_update_competitions.assert_called_once()


def test_purchasePlaces_insufficient_points(mocker, client):
    """
    Test purchasePlaces avec pas assez de points
    Vérifie que la fonction purchasePlaces retourne un code 200 et que le message d'erreur est présent dans la réponse.
    Vérifie que les fonctions updateClubs et updateCompetitions ne sont pas appelées.
    """
    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '10'
    })
    
    assert response.status_code == 200
    assert b"have enough points" in response.data
    mock_update_clubs.assert_not_called()
    mock_update_competitions.assert_not_called()


def test_purchasePlaces_zero_places(mocker, client):
    """
    Test purchasePlaces avec zéro place
    Vérifie que la fonction purchasePlaces retourne un code 200 et que le message d'erreur est présent dans la réponse.
    Vérifie que les fonctions updateClubs et updateCompetitions ne sont pas appelées.
    """
    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '0'
    })
    
    assert response.status_code == 200
    assert b"You cannot book a number of places less than or equal to 0" in response.data
    mock_update_clubs.assert_not_called()
    mock_update_competitions.assert_not_called()


def test_purchasePlaces_negative_places(mocker, client):
    """
    Test purchasePlaces avec un nombre de places négatif.
    Vérifie que la fonction purchasePlaces retourne un code 200 et que le message d'erreur est présent dans la réponse.
    Vérifie que les fonctions updateClubs et updateCompetitions ne sont pas appelées.
    """
    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '-1'
    })
    
    assert response.status_code == 200
    assert b"You cannot book a number of places less than or equal to 0" in response.data
    mock_update_clubs.assert_not_called()
    mock_update_competitions.assert_not_called()


def test_purchasePlaces_not_enough_places(mocker, client):
    """
    Test purchasePlaces avec pas assez de places disponibles
    Vérifie que la fonction purchasePlaces retourne un code 200 et que le message d'erreur est présent dans la réponse.
    Vérifie que les fonctions updateClubs et updateCompetitions ne sont pas appelées.
    """
    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '15'
    })
    
    assert response.status_code == 200
    assert b"There are not enough places available" in response.data
    mock_update_clubs.assert_not_called()
    mock_update_competitions.assert_not_called()

def test_purchasePlaces_points_deduction(mocker, client):
    """
    Test que les points sont correctement déduits après une réservation réussie.
    Vérifie que les points sont déduits dans server.clubs (en mémoire)
    Vérifie que les bonnes données sont passées à updateClubs() (pour sauvegarde JSON)
    """
    mock_update_clubs = mocker.patch('server.updateClubs')
    mocker.patch('server.updateCompetitions')
    
    # Sauvegarder l'état initial depuis server.clubs (après setup_mock_data)
    club_before_deduction = next(club for club in server.clubs if club['name'] == 'She Lifts')
    points_before_deduction = int(club_before_deduction['points'])
    places_to_book = 3
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'She Lifts',
        'places': str(places_to_book)
    })
    
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    
    # Vérification 1 : Les données passées à updateClubs() sont correctes (pour sauvegarde JSON)
    mock_update_clubs.assert_called_once()
    clubs_passed = mock_update_clubs.call_args[0][0] # mock_update_clubs.call_args = (args=(clubs,), kwargs={}) => clubs_passed = clubs
    club_after_deduction = next(club for club in clubs_passed if club['name'] == 'She Lifts')
    points_after_deduction = int(club_after_deduction['points'])
    assert points_after_deduction == points_before_deduction - places_to_book
    
    # Vérification 2 : Les données dans server.clubs sont mises à jour (en mémoire)
    club_in_memory = next(club for club in server.clubs if club['name'] == 'She Lifts')
    assert int(club_in_memory['points']) == points_before_deduction - places_to_book


def test_purchasePlaces_competition_places_deduction(mocker, client):
    """
    Test que les places de la compétition sont correctement déduites.
    Vérifie que les places sont déduites dans server.competitions (en mémoire)
    Vérifie que les bonnes données sont passées à updateCompetitions() (pour sauvegarde JSON)
    """
    mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    
    # Sauvegarder l'état initial depuis server.competitions (après setup_mock_data)
    comp_before_deduction = next(comp for comp in server.competitions if comp['name'] == 'Spring Festival')
    places_before_deduction = int(comp_before_deduction['numberOfPlaces'])
    places_to_book = 2
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': str(places_to_book)
    })
    
    assert response.status_code == 200
            
    # Vérifie que les données passées à updateCompetitions() sont correctes (pour sauvegarde JSON)
    mock_update_competitions.assert_called_once()
    competitions_passed = mock_update_competitions.call_args[0][0] # mock_update_competitions.call_args = (args=(competitions,), kwargs={}) => competitions_passed = competitions
    comp_after_deduction = next(comp for comp in competitions_passed if comp['name'] == 'Spring Festival')
    places_after_deduction = int(comp_after_deduction['numberOfPlaces'])
    assert places_after_deduction == places_before_deduction - places_to_book
    
    # Vérifie que les données dans server.competitions sont mises à jour (en mémoire)
    comp_in_memory = next(comp for comp in server.competitions if comp['name'] == 'Spring Festival')
    assert int(comp_in_memory['numberOfPlaces']) == places_before_deduction - places_to_book


def test_purchasePlaces_other_clubs_not_affected(mocker, client):
    """
    Test que les autres clubs ne sont pas affectés par une réservation.
    Vérifie que les clubs non modifiés sont inchangés dans server.clubs.
    """

    mock_update_clubs = mocker.patch('server.updateClubs')
    mocker.patch('server.updateCompetitions')
    
    clubs_before = {club['name']: int(club['points']) for club in server.clubs}
    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    })
    
    assert response.status_code == 200
    
    mock_update_clubs.assert_called_once()
    clubs_passed = mock_update_clubs.call_args[0][0] 
    clubs_after_dict = {}
    for club in clubs_passed:
        clubs_after_dict[club['name']] = int(club['points'])
    
    #club modifié : Simply Lift
    assert clubs_after_dict['Simply Lift'] == clubs_before['Simply Lift'] - 2

    #clubs non modifiés : Iron Temple et She Lifts
    assert clubs_after_dict['Iron Temple'] == clubs_before['Iron Temple']
    assert clubs_after_dict['She Lifts'] == clubs_before['She Lifts']
