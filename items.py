import db
import sqlite3

def add_item(title, seed, description, user_id, game_id):
    sql = """INSERT INTO items (title, seed, description, user_id, game_id)
    VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, seed, description, user_id, game_id])

def add_game(title, allowed_characters, max_length, use_all, user_id):
    sql = """INSERT INTO games (title, allowed_characters, max_length, use_all, user_id)
    VALUES (?, ?, ?, ?, ?)"""
    try:
        db.execute(sql, [title, allowed_characters, max_length, use_all, user_id])
    except sqlite3.IntegrityError:
        return False
    return True

def get_items():
    sql = "SELECT id, title, seed FROM items ORDER BY id DESC"

    return db.query(sql)

def get_games():
    sql = "SELECT id, title FROM games ORDER BY id DESC"

    return db.query(sql)

def get_item(item_id):
    sql = """
    SELECT
        I.id,
        I.title,
        I.seed,
        I.description,
        I.user_id,
        I.game_id,
        U.username,
        G.title AS game
    FROM
        Items I, Users U, Games G
    WHERE
        I.id = ? AND
        I.user_id = U.id AND
        I.game_id = G.id
    """

    result = db.query(sql, [item_id])
    return result[0] if result else None

def get_game(game_id):
    sql = """
    SELECT
        G.id,
        G.title,
        G.max_length,
        G.allowed_characters,
        G.use_all,
        U.username
    FROM
        Users U, Games G
    WHERE
        G.id = ? AND
        G.user_id = U.id
    """

    result = db.query(sql, [game_id])
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

def find_all_items(game_id):
    sql = """
    SELECT
        id, title
    FROM
        Items
    WHERE
        game_id = ?
    ORDER BY
        id DESC
    """

    return db.query(sql, [game_id])

def find_games(terms):
    sql = """
    SELECT
        id, title
    FROM
        games
    WHERE
        title LIKE ?
    ORDER BY
        id DESC
    """

    terms = "%" + terms + "%"
    return db.query(sql, [terms])

def add_comment(item_id, user_id, comment):
    print(item_id)
    print(user_id)
    print(comment)
    sql = """INSERT INTO comments (item_id, user_id, content, pinned)
    VALUES (?, ?, ?, 0)"""

    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql = """
    SELECT
        C.id,
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

def get_user_commented_posts(user_id):
    sql = """
    SELECT DISTINCT 
        I.id,
        I.title as item_title
    FROM
        Comments C, Items I
    WHERE
        C.item_id = I.id AND
        C.user_id = ?
    ORDER BY
        C.time DESC
    """

    return db.query(sql, [user_id])

def get_comment(comment_id):
    sql = """
    SELECT
        C.id,
        C.content,
        C.user_id,
        C.item_id,
        U.username,
        C.time,
        C.pinned
    FROM
        Comments C, Users U
    WHERE
        C.id = ? AND
        C.user_id = U.id
    """

    result = db.query(sql, [comment_id])
    return result[0] if result else None

def remove_comment(comment_id):
    sql = "DELETE FROM Comments WHERE id = ?"
    db.execute(sql, [comment_id])
