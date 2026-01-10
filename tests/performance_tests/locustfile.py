from locust import HttpUser, task, between
import random



class PerformanceTestUser(HttpUser):
    """
    Simule le comportement d'un utilisateur.
    """
    wait_time = between(1, 3)
    

    TEST_EMAILS = [
        'john@simplylift.co',
        'admin@irontemple.com',
        'kate@shelifts.co.uk'
    ]
    
    TEST_COMPETITIONS = [
        'Spring Festival',
        'Fall Classic'
    ]
    
    def on_start(self):
        self.email = random.choice(self.TEST_EMAILS)
        self.club_name = self._get_club_name_from_email(self.email)
        self.competition_name = random.choice(self.TEST_COMPETITIONS)
    
    def _get_club_name_from_email(self, email):
        """Récupère le nom du club à partir de l'email"""
        email_to_club = {
            'john@simplylift.co': 'Simply Lift',
            'admin@irontemple.com': 'Iron Temple',
            'kate@shelifts.co.uk': 'She Lifts'
        }
        return email_to_club.get(email)
    
    @task
    def view_index(self):
        """
        Tâche : consulter la page d'accueil
        """
        self.client.get("/", name="/")

    @task
    def view_points_board(self):
        """
        Tâche : consulter le tableau des points
        """
        self.client.get("/points_board", name="/points_board")
   
    @task
    def login_and_view_competitions(self):
        """
        Tâche : se connecter et consulter les compétitions
        """
        self.client.post(
            "/showSummary",
            data={"email": self.email},
            name="/showSummary"
        )
    
    @task
    def book_places(self):
        """
        Tâche : aller à la page de réservation
        """
        self.client.get(
            f"/book/{self.competition_name}/{self.club_name}",
            name="/book"
        )
    
    @task
    def purchase_places(self):
        """
        Tâche : effectuer la réservation
        """
        self.client.post(
            "/purchasePlaces",
            data={"competition": self.competition_name, "club": self.club_name, "places": "1"},
            name="/purchasePlaces"
        )

    @task
    def logout(self):
        """Tâche : se déconnecter"""
        self.client.get("/logout", name="/logout")
