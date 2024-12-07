from app import app, db
from sqlalchemy import text

with app.app_context():
    db.create_all()

    db.session.execute(text("CREATE INDEX game_date ON Game(date);"))

    db.session.execute(text("CREATE INDEX game_field_index ON Game(field);"))

    db.session.commit()

    #with db.session.begin():
        #db.session.execute(text("DROP INDEX IF EXISTS idx_game_date;"))
        #db.session.execute(text("DROP INDEX IF EXISTS idx_game_id_field;"))
        #print("indexes removed successfully")

    result = db.session.execute(text("PRAGMA index_list('Game');"))
    indexes = result.fetchall()

    for index in indexes:
        print(index)

    print("Database created successfully")
