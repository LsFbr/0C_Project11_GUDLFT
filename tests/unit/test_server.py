import server
from bs4 import BeautifulSoup

# tests Entering_a_unknown_email_crashes_the_app
def test_showSummary_with_valid_email(mocker):
    """Test showSummary avec un email valide existant dans clubs."""
    email = "club@example.com"
    club = {"name": "Club Example", "email": "club@example.com", "points": "24"}
    competitions = [{"name": "Competition Example", "date": "2026-03-27 10:00:00", "numberOfPlaces": "25"}]
    
    mock_render = mocker.patch("server.render_template")
    mock_flash = mocker.patch("server.flash")
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", competitions)
    
    with server.app.test_request_context(method="POST", data={"email": email}):
        server.showSummary()
    
    mock_render.assert_called_once_with(
        "welcome.html",
        club=club,
        competitions=competitions,
        datetime=server.datetime
    )
    mock_flash.assert_not_called()

def test_showSummary_with_unknown_email(mocker):
    """Test showSummary avec un email qui n'existe pas dans clubs."""
    email = "unknown@example.com"
    club = {"name": "Club Example", "email": "club@example.com", "points": "24"}
    competitions = [{"name": "Competition Example", "date": "2026-03-27 10:00:00", "numberOfPlaces": "25"}]

    mock_render = mocker.patch("server.render_template")
    mock_flash = mocker.patch("server.flash")
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", competitions)
    
    with server.app.test_request_context(method="POST", data={"email": email}):
        server.showSummary()
    
    mock_render.assert_called_once_with("index.html")
    mock_flash.assert_called_once_with("Email not found, please try again")


# tests Clubs_should_not_be_able_to_use_more_than_their_points_allowed

def test_purchasePlaces_success(mocker):
    """Test purchasePlaces avec un nombre de points suffisants"""
    initial_club_points = "24"
    initial_competition_numberOfPlaces = "25"
    club = {"name": "Club Example", "email": "club@example.com", "points": initial_club_points}
    competition = {"name": "Competition Example", "date": "2999-03-27 10:00:00", "numberOfPlaces": initial_competition_numberOfPlaces}
    places_to_book = "2"

    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context(method="POST", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": places_to_book
    }):
        server.purchasePlaces()

    mock_render.assert_called_once_with("welcome.html", club=club, competitions=[competition], datetime=server.datetime)
    mock_flash.assert_called_once_with(f'Great-Booking of {places_to_book} places for {competition["name"]} has been completed!')

def test_purchasePlaces_insufficient_points(mocker):
    """Test purchasePlaces avec un nombre de points suffisants"""
    initial_club_points = "1"
    initial_competition_numberOfPlaces = "25"
    club = {"name": "Club Example", "email": "club@example.com", "points": initial_club_points}
    competition = {"name": "Competition Example", "date": "2999-03-27 10:00:00", "numberOfPlaces": initial_competition_numberOfPlaces}
    places_to_book = "2"

    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context(method="POST", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": places_to_book
    }):
        server.purchasePlaces()

    mock_render.assert_called_once_with("booking.html", club=club, competition=competition)
    mock_flash.assert_called_once_with("You don't have enough points to book this number of places")

def test_purchasePlaces_zero_places(mocker):
    """Test purchasePlaces avec zéro place"""
    initial_club_points = "1"
    initial_competition_numberOfPlaces = "25"
    club = {"name": "Club Example", "email": "club@example.com", "points": initial_club_points}
    competition = {"name": "Competition Example", "date": "2999-03-27 10:00:00", "numberOfPlaces": initial_competition_numberOfPlaces}
    places_to_book = "0"

    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context(method="POST", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": places_to_book
    }):
        server.purchasePlaces()

    mock_render.assert_called_once_with("booking.html", club=club, competition=competition)
    mock_flash.assert_called_once_with("You cannot book a number of places less than or equal to 0")

# tests Clubs_should_not_be_able_to_book_more_than_the_competition_places_available
def test_purchasePlaces_not_enough_places(mocker):
    """Test purchasePlaces avec pas assez de places disponibles"""
    initial_club_points = "24"
    initial_competition_numberOfPlaces = "1"
    club = {"name": "Club Example", "email": "club@example.com", "points": initial_club_points}
    competition = {"name": "Competition Example", "date": "2999-03-27 10:00:00", "numberOfPlaces": initial_competition_numberOfPlaces}
    places_to_book = "2"

    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context(method="POST", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": places_to_book
    }):
        server.purchasePlaces()

    mock_render.assert_called_once_with("booking.html", club=club, competition=competition)
    mock_flash.assert_called_once_with("There are not enough places available")

# tests Clubs_shouldn't_be_able_to_book_more_than_12_places_per_competition
def test_purchasePlaces_more_than_12_places(mocker):
    """Test purchasePlaces avec plus de 12 places"""
    initial_club_points = "24"
    initial_competition_numberOfPlaces = "25"
    club = {"name": "Club Example", "email": "club@example.com", "points": initial_club_points}
    competition = {"name": "Competition Example", "date": "2999-03-27 10:00:00", "numberOfPlaces": initial_competition_numberOfPlaces}
    places_to_book = "13"

    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context(method="POST", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": places_to_book
    }):
        server.purchasePlaces()

    mock_render.assert_called_once_with("booking.html", club=club, competition=competition)
    mock_flash.assert_called_once_with("You cannot book more than 12 places at a time")

# tests Booking_places_in_past_competitions
def test_book_with_past_competition(mocker):
    """Test book avec une compétition passée"""
    club = {"name": "Club Example", "email": "club@example.com", "points": "24"}
    competition = {"name": "Competition Example", "date": "2000-03-27 10:00:00", "numberOfPlaces": "25"}

    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context():
        server.book(competition["name"], club["name"])

    mock_render.assert_called_once_with("welcome.html", club=club, competitions=[competition], datetime=server.datetime)
    mock_flash.assert_called_once_with("Cannot book places for past competitions")

def test_book_with_future_competition(mocker):
    """Test book avec une compétition future"""
    club = {"name": "Club Example", "email": "club@example.com", "points": "24"}
    competition = {"name": "Competition Example", "date": "2999-03-27 10:00:00", "numberOfPlaces": "25"}

    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context():
        server.book(competition["name"], club["name"])

    mock_render.assert_called_once_with("booking.html", club=club, competition=competition)
    mock_flash.assert_not_called()

def test_purchasePlaces_with_past_competition(mocker):
    """Test purchasePlaces avec une compétition passée"""
    initial_club_points = "24"
    initial_competition_numberOfPlaces = "25"
    club = {"name": "Club Example", "email": "club@example.com", "points": initial_club_points}
    competition = {"name": "Competition Example", "date": "2000-03-27 10:00:00", "numberOfPlaces": initial_competition_numberOfPlaces}
    places_to_book = "2"

    mock_update_clubs = mocker.patch('server.updateClubs')
    mock_update_competitions = mocker.patch('server.updateCompetitions')
    mock_render = mocker.patch('server.render_template')
    mock_flash = mocker.patch('server.flash')
    mocker.patch.object(server, "clubs", [club])
    mocker.patch.object(server, "competitions", [competition])

    with server.app.test_request_context(method="POST", data={
        "competition": competition["name"],
        "club": club["name"],
        "places": places_to_book
    }):
        server.purchasePlaces()

    mock_render.assert_called_once_with("welcome.html", club=club, competitions=[competition], datetime=server.datetime)
    mock_flash.assert_called_once_with("Cannot book places for past competitions")

# purchasePlaces tests

#def test_purchasePlaces_points_deduction(mocker, client):
#    """
#    Test que les points sont correctement déduits après une réservation réussie.
#    Vérifie que les points sont déduits dans server.clubs (en mémoire)
#    Vérifie que les bonnes données sont passées à updateClubs() (pour sauvegarde JSON)
#    """
#    mock_update_clubs = mocker.patch('server.updateClubs')
#    mocker.patch('server.updateCompetitions')
#    
#    # Sauvegarder l'état initial depuis server.clubs (après setup_mock_data)
#    club_before_deduction = next(club for club in server.clubs if club['name'] == 'She Lifts')
#    points_before_deduction = int(club_before_deduction['points'])
#    places_to_book = 3
#    
#    response = client.post('/purchasePlaces', data={
#        'competition': 'Fall Classic',
#        'club': 'She Lifts',
#        'places': str(places_to_book)
#    })
#    
#    assert response.status_code == 200
#    assert b'Great-Booking of 3 places for Fall Classic has been completed!' in response.data
#    
#    # Vérification 1 : Les données passées à updateClubs() sont correctes (pour sauvegarde JSON)
#    mock_update_clubs.assert_called_once()
#    clubs_passed = mock_update_clubs.call_args[0][0] # mock_update_clubs.call_args = (args=(clubs,), kwargs={}) => clubs_passed = clubs
#    club_after_deduction = next(club for club in clubs_passed if club['name'] == 'She Lifts')
#    points_after_deduction = int(club_after_deduction['points'])
#    assert points_after_deduction == points_before_deduction - places_to_book
#    
#    # Vérification 2 : Les données dans server.clubs sont mises à jour (en mémoire)
#    club_in_memory = next(club for club in server.clubs if club['name'] == 'She Lifts')
#    assert int(club_in_memory['points']) == points_before_deduction - places_to_book


#def test_purchasePlaces_competition_places_deduction(mocker, client):
#    """
#    Test que les places de la compétition sont correctement déduites.
#    Vérifie que les places sont déduites dans server.competitions (en mémoire)
#    Vérifie que les bonnes données sont passées à updateCompetitions() (pour sauvegarde JSON)
#    """
#    mocker.patch('server.updateClubs')
#    mock_update_competitions = mocker.patch('server.updateCompetitions')
#    
#    # Sauvegarder l'état initial depuis server.competitions (après setup_mock_data)
#    comp_before_deduction = next(comp for comp in server.competitions if comp['name'] == 'Spring Festival')
#    places_before_deduction = int(comp_before_deduction['numberOfPlaces'])
#    places_to_book = 2
#    
#    response = client.post('/purchasePlaces', data={
#        'competition': 'Spring Festival',
#        'club': 'Simply Lift',
#        'places': str(places_to_book)
#    })
#    
#    assert response.status_code == 200
#            
#    # Vérifie que les données passées à updateCompetitions() sont correctes (pour sauvegarde JSON)
#    mock_update_competitions.assert_called_once()
#    competitions_passed = mock_update_competitions.call_args[0][0] # mock_update_competitions.call_args = (args=(competitions,), kwargs={}) => competitions_passed = competitions
#    comp_after_deduction = next(comp for comp in competitions_passed if comp['name'] == 'Spring Festival')
#    places_after_deduction = int(comp_after_deduction['numberOfPlaces'])
#    assert places_after_deduction == places_before_deduction - places_to_book
#    
#    # Vérifie que les données dans server.competitions sont mises à jour (en mémoire)
#    comp_in_memory = next(comp for comp in server.competitions if comp['name'] == 'Spring Festival')
#    assert int(comp_in_memory['numberOfPlaces']) == places_before_deduction - places_to_book
#
#
#def test_purchasePlaces_other_clubs_not_affected(mocker, client):
#    """
#    Test que les autres clubs ne sont pas affectés par une réservation.
#    Vérifie que les clubs non modifiés sont inchangés dans server.clubs.
#    """
#
#    mock_update_clubs = mocker.patch('server.updateClubs')
#    mocker.patch('server.updateCompetitions')
#    
#    clubs_before = {club['name']: int(club['points']) for club in server.clubs}
#    
#    response = client.post('/purchasePlaces', data={
#        'competition': 'Spring Festival',
#        'club': 'Simply Lift',
#        'places': '2'
#    })
#    
#    assert response.status_code == 200
#    
#    mock_update_clubs.assert_called_once()
#    clubs_passed = mock_update_clubs.call_args[0][0] 
#    clubs_after_dict = {}
#    for club in clubs_passed:
#        clubs_after_dict[club['name']] = int(club['points'])
#    
#    #club modifié : Simply Lift
#    assert clubs_after_dict['Simply Lift'] == clubs_before['Simply Lift'] - 2
#
#    #clubs non modifiés : Iron Temple et She Lifts
#    assert clubs_after_dict['Iron Temple'] == clubs_before['Iron Temple']
#    assert clubs_after_dict['She Lifts'] == clubs_before['She Lifts']
#
#

# points_board tests
#def test_points_board_accessible_without_authentication(client):
#    """
#    Test que la route points_board est accessible sans authentification
#    Vérifie que la fonction points_board retourne un code 200.
#    """
#    response = client.get('/points_board')
#    assert response.status_code == 200
#
#
#def test_points_board_displays_all_clubs(client):
#    """
#    Test que tous les clubs sont affichés dans le tableau
#    Vérifie que les noms de tous les clubs sont présents dans la réponse.
#    """
#    response = client.get('/points_board')
#    assert response.status_code == 200
#    for club in server.clubs:
#        assert club['name'].encode() in response.data
#
#
#def test_points_board_displays_all_points(client):
#    """
#    Test que tous les points des clubs sont affichés correctement
#    Vérifie que les points de tous les clubs sont présents dans la réponse.
#    """
#    response = client.get('/points_board')
#    assert response.status_code == 200
#    for club in server.clubs:
#        assert club['points'].encode() in response.data