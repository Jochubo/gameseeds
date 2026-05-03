import re
import markupsafe
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
from secrets import token_hex
import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    terms = request.args.get("terms")

    if terms:
        all_games = items.find_games(terms)
    else:
        all_games = items.get_games()

    if not terms:
        terms = ""

    return render_template("index.html", games=all_games, terms=terms)

@app.route("/game/<int:game_id>")
def show_game(game_id):
    game = items.get_game(game_id)
    terms = request.args.get("terms")

    if terms:
        all_items = items.find_items(terms, game_id)
    else:
        all_items = items.find_all_items(game_id)
        terms = ""

    return render_template("show_game.html", items=all_items, terms=terms, game=game)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    posts = users.get_items(user_id)
    comments = items.get_user_commented_posts(user_id)
    return render_template("show_user.html", user=user, items=posts, comments=comments)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    comments = items.get_comments(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item, comments=comments)

@app.route("/game/<int:game_id>/new_item")
def new_item(game_id):
    require_login()

    game = items.get_game(game_id)
    regex = config.regex_expressions[game["allowed_characters"]]
    return render_template("new_item.html", game=game, regex=regex)

@app.route("/new_game")
def new_game():
    require_login()

    return render_template("new_game.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    title = request.form["title"]
    seed = request.form["seed"]
    description = request.form["description"]
    game_id = request.form["game_id"]
    user_id = session["user_id"]

    if not (title or seed or description or game_id):
        abort(403)

    game = items.get_game(game_id)
    regex = config.regex_expressions[game["allowed_characters"]]

    if len(title) > 50 or len(description) > 1000:
        abort(403)
    elif len(seed) > game["max_length"]:
        abort(403)
    elif not re.search(regex, seed):
        abort(403)

    elif len(seed) != game["max_length"] and game["use_all"]:
        flash(game["title"] + " seeds cannot have blank characters")
        return redirect("/game/" + str(game_id) + "/new_item")

    items.add_item(title, seed, description, user_id, game_id)
    flash("Post created successfully")
    return redirect("/game/" + str(game_id))

@app.route("/create_game", methods=["POST"])
def create_game():
    require_login()
    check_csrf()

    title = request.form["title"]
    allowed_characters = request.form["allowed_characters"]
    max_length = int(request.form["max_length"])
    use_all = "use_all" in request.form
    user_id = session["user_id"]

    if len(title) > 50 or max_length > 100 or max_length < 1:
        abort(403)
    elif not (title or allowed or max_length or use_all):
        abort(403)

    use_all = 1 if use_all else 0
    if items.add_game(title, allowed_characters, max_length, use_all, user_id):
        flash("Game added successfully")
        return redirect("/")
    flash("ERROR: Game exists already", "error")
    return redirect("/new_game")

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]
    item_id = request.form["item_id"]
    user_id = session["user_id"]

    if len(comment) > 400:
        abort(403)
    item = items.get_item(item_id)
    if not (comment or item):
        abort(403)

    items.add_comment(item_id, user_id, comment)
    return redirect("/item/" + str(item_id))

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
    check_csrf()

    user_id = int(request.form["user_id"])
    item_id = request.form["item_id"]
    title = request.form["title"]
    description = request.form["description"]

    if not title or not description:
        abort(403)
    elif user_id != session["user_id"]:
        abort(403)
    elif len(title) > 50:
        abort(403)
    elif len(description) > 1000:
        abort(403)

    items.update_item(item_id, title, description)
    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        if "remove" in request.form:
            check_csrf()
            items.remove_item(item_id)
            flash("Post deleted successfully")
            return redirect("/game/" + str(item["game_id"]))
        else:
            return redirect("/item/" + str(item_id))

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = items.get_comment(comment_id)

    if request.method == "GET":
        if not comment:
            abort(404)
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        if "remove" in request.form:
            check_csrf()
            items.remove_comment(comment_id)
        return redirect("/item/" + str(comment["item_id"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("ERROR: Passwords do not match", "error")
            return render_template("register.html")

        if not users.create_user(username, password1):
            flash("ERROR: username already exists", "error")
            return render_template("register.html")

        flash("Account created successfully")
        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)

        if user_id:
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = token_hex(16)
            flash("Successfully logged in")
            return redirect("/")

        else:
            flash("ERROR: Invalid password or username", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        flash("Successfully logged out")
    return redirect("/")
