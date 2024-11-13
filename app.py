from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for the Game
class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    score = db.Column(db.String(20), nullable=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)


# Home page that displays the list of games and the fields to add a game
@app.route("/", methods=['GET', 'POST'])
def home():
    game_to_edit = None

    if request.method == 'POST':
        game_id = request.form.get('game_id')
        field = request.form['field']
        date = request.form['date']
        score = request.form['score']
        home_team = request.form['home_team']
        away_team = request.form['away_team']

        if game_id:
            game = Game.query.get(game_id)
            game.field = field
            game.date = date
            game.score = score
            game.home_team = home_team
            game.away_team = away_team
            db.session.commit()
        else:
            new_game = Game(field=field, date=date, score=score, home_team=home_team, away_team=away_team)
            db.session.add(new_game)
            db.session.commit()

        return redirect("/")

    if request.args.get('game_id'):
        game_id = request.args.get('game_id')
        game_to_edit = Game.query.get(game_id)

    games = Game.query.all()
    return render_template("games.html", rows=games, game_to_edit=game_to_edit)


# Route to handle editing a game
@app.route("/edit/<int:game_id>")
def edit(game_id):
    game_to_edit = Game.query.get(game_id)
    
    if not game_to_edit:
        return "Game not found", 404

    
    return render_template("games.html", rows=[], game_to_edit=game_to_edit)


#Route to handle deleting a game
@app.route("/delete/<int:game_id>", methods=['POST'])
def delete(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
