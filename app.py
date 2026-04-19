import sqlite3
import re
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    query = request.args.get("query")
    if query:
        all_items = items.find_items(query)
    else:
        all_items = items.get_items()
        query = ""
    return render_template("index.html", items=all_items, query=query)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item)

@app.route("/new_item")
def new_item():
    require_login()

    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()

    title = request.form["title"]
    seed = request.form["seed"]
    description = request.form["description"]
    game = request.form["game"]
    user_id = session["user_id"]

    if len(title) > 50 or len(seed) > 50 or len(game) > 50:
        abort(403)
    elif len(description) > 1000:
        abort(403)
    elif not title or seed or game or description:
        abort(403)
    elif not re.search("^[0-9]{0,50}$", seed):
        abort(403)

    items.add_item(title, seed, description, user_id, game)
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    title = request.form["title"]
    description = request.form["description"]

    if item_id != session["user_id"]:
        abort(403)
    if len(title) > 50:
        abort(403)
    elif len(description) > 1000:
        abort(403)
    elif not title or description:
        abort(403)

    items.update_item(item_id, title, description)
    return redirect("/")

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    if request.method == "GET":
        item = items.get_item(item_id)
        if not item:
            abort(404)
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: Passwords do not match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username already exists"

    return "Account registered"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "ERROR: Incorrect username or password"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
