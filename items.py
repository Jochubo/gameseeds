import db

def add_item(title, seed, description, user_id, game):
    sql = "SELECT id FROM games WHERE name = ?"
    game_id = db.query(sql, [game])[0][0]

    sql = """INSERT INTO items (title, seed, description, user_id, game_id)
    VALUES (?, ?, ?, ?, ?)"""
    db. execute(sql, [title, seed, description, user_id, game_id])
