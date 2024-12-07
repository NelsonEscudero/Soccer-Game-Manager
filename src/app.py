from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

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

    distinct_fields = db.session.execute(text("SELECT DISTINCT field FROM Game ORDER BY field")).fetchall()
    fields = [row.field for row in distinct_fields]

    current_year = datetime.now().year
    year_range = range(current_year - 10, current_year + 5)
    games = Game.query.all()
    return render_template(
        "games.html",
        rows=games,
        game_to_edit=None,
        years=year_range,
        fields=fields,
        selected_month=0,
        selected_day=0,
        selected_year=0,
        selected_field=-1
    )

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


#Route to handle filtering games by date
@app.route("/filter", methods=['GET'])
def filter():
    month = request.args.get('month')
    day = request.args.get('day')      
    year = request.args.get('year') 
    field = request.args.get('field')

    fields = []
    current_year = datetime.now().year
    year_range = range(current_year - 10, current_year + 5)
    
    
    if (not (month and day and year)) and field:
        if field != "All":
            field_query = f"SELECT * FROM Game WHERE field = '{field}'"
        else:
            return redirect('/')
             
        result = db.session.execute(text(field_query)).mappings()

        games = [
            {
                "game_id": row["game_id"],
                "field": row["field"],
                "date": row["date"],
                "score": row["score"],
                "home_team": row["home_team"],
                "away_team": row["away_team"]
            }
            for row in result
        ]

        num_results = len(games)
        total_goals = 0
        num_scores = 0

        for game in games:
            if game["score"]:
                try:
                    home_goals, away_goals = map(int, game["score"].split('-'))
                    total_goals += home_goals + away_goals
                    num_scores += 1
                except ValueError:
                    continue
    
        if (num_scores > 0):
            avg_goals = total_goals / num_scores
        else:
            avg_goals = 0

        return render_template(
            "games.html",
            rows=games,
            game_to_edit=None,
            years=year_range,
            selected_month=month,
            selected_day=day,
            selected_year=year,
            selected_field=field,
            num_results=num_results,
            avg_goals=avg_goals
        )
    elif not (month and day and year and field):
        return redirect('/')

    date = f"{int(month):02}/{int(day):02}/{year}"
    field_query = ""

    #Prepared statements to query the database using the index on the date
    if field != "All":
        field_query = f"SELECT * FROM Game WHERE field = '{field}'"
    else:
        field_query = f"SELECT * FROM Game"
    date_query = f"SELECT * FROM Game WHERE date = '{date}'"

    final_query = f"""{field_query} INTERSECT {date_query}"""

    result = db.session.execute(text(final_query)).mappings()

    games = [
        {
            "game_id": row["game_id"],
            "field": row["field"],
            "date": row["date"],
            "score": row["score"],
            "home_team": row["home_team"],
            "away_team": row["away_team"]
        }
        for row in result
    ]

    num_results = len(games)
    total_goals = 0
    num_scores = 0

    for game in games:
        if game["score"]:
            try:
                home_goals, away_goals = map(int, game["score"].split('-'))
                total_goals += home_goals + away_goals
                num_scores += 1
            except ValueError:
                continue
    
    if (num_scores > 0):
        avg_goals = total_goals / num_scores
    else:
        avg_goals = 0


    if field == "All":
        filtered_field_query = f"SELECT DISTINCT field FROM ({final_query}) ORDER BY field"
        distinct_fields = db.session.execute(text(filtered_field_query)).fetchall()
        fields = [row.field for row in distinct_fields]

        return render_template(
            "games.html",
            rows=games,
            game_to_edit=None,
            years=year_range,
            fields=fields,
            selected_month=month,
            selected_day=day,
            selected_year=year,
            selected_field=field,
            num_results=num_results,
            avg_goals=avg_goals
        )
    
    filtered_field_query = f"SELECT DISTINCT field FROM ({date_query}) ORDER BY field"
    distinct_fields = db.session.execute(text(filtered_field_query)).fetchall()
    fields = [row.field for row in distinct_fields]

    return render_template(
        "games.html",
        rows=games,
        game_to_edit=None,
        years=year_range,
        fields=fields,
        selected_month=month,
        selected_day=day,
        selected_year=year,
        selected_field=field,
        num_results=num_results,
        avg_goals=avg_goals
    )