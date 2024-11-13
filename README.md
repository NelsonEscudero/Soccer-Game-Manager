# Soccer-Game-Manager
This is a small web application in Python and HTML that allows a user to add soccer games and all the 
information associated with the game. When a user submits a game all the data gets stored in a MySQL 
database and the user will see a list of games that they've added, being able to edit and delete them
as well.

## Frontend Info
This application uses HTML and Flask to build and run the web app, rendering different templates certain routes are accessed and displaying live data.

## Backend Info
Uses a MySQL relational database and SQLAlchemy to access and manage the database using Python objects. 

## Build
1. First set up a virtual environment in the local repository
2. On Windows activate you virtual environment by running '.venv\Scripts\activate', or on macOS/Linux run 'source .venv/bin/activate'
3. Then install Flask: 'pip install Flask'
4. Then set Flask environment variable: 'set FLASK_APP=app.py'
5. Then install SQLAlchemy: 'pip install SQLAlchemy'
6. Then install Flask-SQLAlchemy: 'pip install Flask-SQLAlchemy'
7. Then go into the src folder and run 'flask run' to start the FLask server and website
 
