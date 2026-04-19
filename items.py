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
        I.id,
        I.title,
        I.seed,
        I.description,
        I.user_id,
        U.username,
        G.name AS game
    FROM
        Items I, Users U, Games G
    WHERE
        I.id = ? AND
        I.user_id = U.id AND
        I.game_id = G.id
    """

    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description):
    sql = """
    UPDATE
        Items
    SET
        title = ?,
        description = ?
    WHERE
        id = ?
    """

    db.execute(sql, [title, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM Items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(terms, game_id):
    sql = """
    SELECT
        id, title
    FROM
        Items
    WHERE
        game_id = ? AND
        (description LIKE ? OR
        title LIKE ?)
    ORDER BY
        id DESC
    """

    terms = "%" + terms + "%"
    return db.query(sql, [game_id, terms, terms])

def add_comment(item_id, user_id, comment):
    print(item_id)
    print(user_id)
    print(comment)
    sql = """INSERT INTO comments (item_id, user_id, content, pinned)
    VALUES (?, ?, ?, 0)"""

    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql ="""
    SELECT
        C.content,
        U.username,
        C.user_id,
        C.time,
        C.pinned
    FROM
        Comments C, Users U
    WHERE
        C.item_id = ? AND
        C.user_id = U.id
    ORDER BY
        C.pinned,
        C.id DESC
    """

    return db.query(sql, [item_id])
