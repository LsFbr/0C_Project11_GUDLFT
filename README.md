# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     
    * [pytest](https://docs.pytest.org/) - Testing framework for running unit and integration tests

    * [coverage](https://coverage.readthedocs.io/) - Code coverage measurement tool

    * [Locust](https://locust.io/) - Performance and load testing framework

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, activate the virtual environment. The command depends on your operating system:
        * **Linux/Mac**: <code>source bin/activate</code>
        * **Windows PowerShell**: <code>.\Scripts\Activate</code>
        * **Windows CMD**: <code>Scripts\activate</code>
      You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - You should now be ready to test the application. In the directory, type <code>flask --app server.py run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing
    We use pytest to run the tests.
    to run the tests globally, type <code>pytest</code>.
    to run the unit tests, type <code>pytest tests/unit/test_server.py</code>.
    to run the integration tests, type <code>pytest tests/integration/test_server.py</code>.

    We use coverage to measure the code coverage.
    to run the tests with coverage and generate the coverage report, type <code>pytest --cov=. --cov-report html</code>.
    the coverage report will be generated in the <code>reports/coverage</code> directory.

    We use Locust for performance testing.
    According to functional specifications:
    - Loading time must not exceed 5 seconds
    - Update time must not exceed 2 seconds
    - Default number of users: 6
    
    Before running performance tests, make sure the app is running. 
    /!\The performance tests use the real test data (`clubs.json` and `competitions.json`). You may need to reset the data after each test run.
    to run the performance tests and generate a report, type <code>locust -f tests/performance_tests/locustfile.py --config=tests/performance_tests/locust.conf --host=http://127.0.0.1:5000</code>.
    the report will be generated in the <code>reports/locust</code> directory.

6. Git Branches

    This project uses a branching strategy to organize bug fixes and features:

    * **master** - Main branch containing the stable version of the application

    * **bug/** - Branches dedicated to bug fixes:
        * `bug/Entering_a_unknown_email_crashes_the_app` - Fix for app crash when entering unknown email
        * `bug/Clubs_should_not_be_able_to_use_more_than_their_points_allowed` - Fix for clubs using more points than allowed
        * `bug/Clubs_should_not_be_able_to_book_more_than_the_competition_places_available` - Fix for clubs booking more places than available
        * `bug/Clubs_shouldn't_be_able_to_book_more_than_12_places_per_competition` - Fix for clubs booking more than 12 places per competition
        * `bug/Booking_places_in_past_competitions` - Fix for booking places in past competitions
        * `bug/Point_updates_are_not_reflected` - Fix for point updates not being reflected

    * **feature/** - Branches dedicated to new features:
        * `feature/Implement_points_display_board` - Implementation of points display board

    * **test/** - Branches dedicated to testing:
        * `test/performances` - Performance testing branch