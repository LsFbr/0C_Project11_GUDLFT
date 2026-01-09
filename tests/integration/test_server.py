import json
import server
from bs4 import BeautifulSoup


def test_complete_user_booking_scenario(client, temp_json_files):
    """
    Test fonctionnel du scénario complet :
    1. Un utilisateur se connecte avec son email
    2. Il consulte les compétitions disponibles
    3. Il réserve 2 places pour une compétition
    4. Il se déconnecte
    5. Il se reconnecte
    6. Vérification : ses points ont bien été déduits et les places réservées
    """
    clubs_file = temp_json_files['clubs_file']
    competitions_file = temp_json_files['competitions_file']
    
    # ÉTAPE 1 : Connexion avec l'email
    email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': email})
    
    assert response.status_code == 200, "La connexion doit réussir"
    assert b'Welcome' in response.data, "Le message de bienvenue doit être affiché"
    assert email.encode() in response.data, "L'email doit être affiché"
    
    # Récupérer les points initiaux depuis le fichier JSON
    with open(clubs_file) as f:
        initial_clubs_data = json.load(f)
    initial_points = int(next(
        c['points'] for c in initial_clubs_data['clubs'] 
        if c['email'] == email
    ))
    
    # Récupérer les places initiales de la compétition
    competition_name = 'Spring Festival'
    with open(competitions_file) as f:
        initial_competitions_data = json.load(f)
    initial_competition_places = int(next(
        c['numberOfPlaces'] for c in initial_competitions_data['competitions']
        if c['name'] == competition_name
    ))
    
    # ÉTAPE 2 : Consultation des compétitions disponibles
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Vérifier que les compétitions sont affichées
    assert competition_name in response.data.decode(), "La compétition doit être affichée"
    
    # Vérifier que le bouton "Book Places" est présent pour les compétitions futures
    book_links = soup.find_all('a', string='Book Places')
    assert len(book_links) > 0, "Le bouton Book Places doit être présent pour les compétitions futures"
    
    # ÉTAPE 3 : Réservation de 2 places pour une compétition
    places_to_book = 2
    club_name = 'Simply Lift'
    
    # Accéder à la page de réservation
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200, "La page de réservation doit être accessible"
    assert competition_name.encode() in response.data, "Le nom de la compétition doit être affiché"
    
    # Effectuer la réservation
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': str(places_to_book)
    })
    
    assert response.status_code == 200, "La réservation doit réussir"
    assert b'Great-Booking' in response.data, "Le message de confirmation doit être affiché"
    assert str(places_to_book).encode() in response.data, "Le nombre de places réservées doit être affiché"
    
    # Vérifier que les fichiers JSON ont été modifiés immédiatement après la réservation
    with open(clubs_file) as f:
        after_booking_clubs_data = json.load(f)
    points_after_booking = int(next(
        c['points'] for c in after_booking_clubs_data['clubs']
        if c['email'] == email
    ))
    
    with open(competitions_file) as f:
        after_booking_competitions_data = json.load(f)
    places_after_booking = int(next(
        c['numberOfPlaces'] for c in after_booking_competitions_data['competitions']
        if c['name'] == competition_name
    ))
    
    assert points_after_booking == initial_points - places_to_book, \
        f"Les points doivent être déduits : {initial_points} - {places_to_book} = {points_after_booking}"
    assert places_after_booking == initial_competition_places - places_to_book, \
        f"Les places doivent être déduites : {initial_competition_places} - {places_to_book} = {places_after_booking}"
    
    # ÉTAPE 4 : Déconnexion (simulée en rechargeant les données depuis les fichiers)
    # Dans une vraie application, cela simulerait une nouvelle session
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    
    # Vérifier que les données en mémoire sont synchronisées avec les fichiers
    club_in_memory = next(c for c in server.clubs if c['email'] == email)
    assert int(club_in_memory['points']) == points_after_booking, \
        "Les données en mémoire doivent être synchronisées avec les fichiers"
    
    # ÉTAPE 5 : Reconnexion
    response = client.post('/showSummary', data={'email': email})
    
    assert response.status_code == 200, "La reconnexion doit réussir"
    assert b'Welcome' in response.data, "Le message de bienvenue doit être affiché"
    assert email.encode() in response.data, "L'email doit être affiché"
    
    # ÉTAPE 6 : Vérification que les points ont bien été déduits
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Vérifier que les points affichés correspondent aux points déduits
    # Les points doivent être affichés quelque part dans la page
    points_displayed = str(points_after_booking).encode()
    assert points_displayed in response.data, \
        f"Les points déduits ({points_after_booking}) doivent être affichés après reconnexion"
    
    # Vérifier dans le fichier JSON que les modifications persistent
    with open(clubs_file) as f:
        final_clubs_data = json.load(f)
    final_points = int(next(
        c['points'] for c in final_clubs_data['clubs']
        if c['email'] == email
    ))
    
    with open(competitions_file) as f:
        final_competitions_data = json.load(f)
    final_places = int(next(
        c['numberOfPlaces'] for c in final_competitions_data['competitions']
        if c['name'] == competition_name
    ))
    
    # Vérifications finales
    assert final_points == initial_points - places_to_book, \
        f"Les points doivent persister après reconnexion : {initial_points} - {places_to_book} = {final_points}"
    assert final_places == initial_competition_places - places_to_book, \
        f"Les places réservées doivent persister : {initial_competition_places} - {places_to_book} = {final_places}"
    
    # Vérifier que les données en mémoire correspondent toujours aux fichiers
    club_final_memory = next(c for c in server.clubs if c['email'] == email)
    competition_final_memory = next(c for c in server.competitions if c['name'] == competition_name)
    
    assert int(club_final_memory['points']) == final_points, \
        "Les points en mémoire doivent correspondre aux fichiers"
    assert int(competition_final_memory['numberOfPlaces']) == final_places, \
        "Les places en mémoire doivent correspondre aux fichiers"
    
    print(f"\n✓ Scénario complet validé :")
    print(f"  - Points initiaux : {initial_points}")
    print(f"  - Points après réservation : {points_after_booking}")
    print(f"  - Points après reconnexion : {final_points}")
    print(f"  - Places initiales : {initial_competition_places}")
    print(f"  - Places après réservation : {places_after_booking}")
    print(f"  - Places après reconnexion : {final_places}")

