import db

def add_item(title, seed, description, user_id, game):
    sql = "SELECT id FROM games WHERE name = ?"
    game_id = db.query(sql, [game])[0][0]

    sql = """INSERT INTO items (title, seed, description, user_id, game_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, seed, description, user_id, game_id])

def get_items():
    sql = "SELECT id, title, seed FROM items ORDER BY id DESC"

    return db.query(sql)

def get_item(item_id):
    sql = """
    SELECT
        I.title,
        I.seed,
        I.description,
        U.username,
        G.name AS game
    FROM
        Items I, Users U, Games G
    WHERE
        I.id = ? AND
        I.user_id = U.id AND
        I.game_id = G.id
    """

    return db.query(sql, [item_id])[0]
