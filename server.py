import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def updateClubs(clubs):
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)

def updateCompetitions(competitions):
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = next((club for club in clubs if club['email'] == request.form['email']), None)

    if club:
        return render_template('welcome.html',club=club,competitions=competitions,datetime=datetime)
    else:
        flash("Email not found, please try again")
        return render_template('index.html')

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        # Vérifier que la compétition est dans le futur
        competition_date = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date.timestamp() <= datetime.now().timestamp():
            flash("Cannot book places for past competitions")
            return render_template('welcome.html', club=foundClub, competitions=competitions, datetime=datetime)
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Vérifier que la compétition est dans le futur
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_date.timestamp() <= datetime.now().timestamp():
        flash("Cannot book places for past competitions")
        return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)

    if placesRequired <= 0:
        flash("You cannot book a number of places less than or equal to 0")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > 12:
        flash("You cannot book more than 12 places at a time")
        return render_template('booking.html', club=club, competition=competition)
    
    if int(club['points']) < placesRequired:
        flash("You don't have enough points to book this number of places")
        return render_template('booking.html', club=club, competition=competition)

    if int(competition['numberOfPlaces']) < placesRequired:
        flash("There are not enough places available")
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces'])-placesRequired)
    updateCompetitions(competitions)
    club['points'] = str(int(club['points'])-placesRequired)
    updateClubs(clubs)

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))