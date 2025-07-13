from io import TextIOWrapper
import os
import datetime
import random
import csv

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///fleshka.db")
deck_icons = {
    1: "􀛮",
    2: "􀆪",
    3: "􀬚",
    4: "􀉛",
    5: "􀌫",
    6: "􀉥"
}


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign user up"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 403)

        elif not password:
            return apology("must provide password", 403)

        elif not confirmation or confirmation != password:
            return apology("must provide a correct password confirmation", 403)

        try:
            db.execute("INSERT INTO users (username, hash, profile_pic_id) VALUES (?, ?, ?)",
                       username, generate_password_hash(password), random.randint(1, 8))

        except ValueError:
            return apology("must provide unique username", 403)

        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username IS ?", username)[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("provide username", 403)

        elif not request.form.get("password"):
            return apology("provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route('/logout', methods=['POST'])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.context_processor
def inject_user_data():
    if "user_id" in session:
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"])
        if user:
            # Add streak_icon depending on today's session
            last_session = db.execute(
                "SELECT MAX(log_date) as last FROM sessions WHERE user_id = ?",
                session["user_id"]
            )[0]["last"]

            if last_session and datetime.datetime.fromisoformat(last_session).date() == datetime.date.today():
                user[0]["streak_icon"] = "active"
            else:
                user[0]["streak_icon"] = "def"
            return dict(user=user[0])
    return dict(user=None)


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


@app.route("/create_deck", methods=["POST"])
@login_required
def create_deck():
    name = request.form.get("name")
    icon = request.form.get("icon")
    color = request.form.get("color")

    db.execute(
        "INSERT INTO decks (name, user_id, icon, color) VALUES (?, ?, ?, ?)",
        name, session["user_id"], icon, color
    )

    return redirect("/")


@app.route("/add_card", methods=["POST"])
@login_required
def add_card():
    question = request.form.get("question")
    answer = request.form.get("answer")
    deck_id = request.form.get("deck_id")

    if not question or not answer or not deck_id:
        return apology("missing data", 400)

    db.execute(
        "INSERT INTO cards (deck_id, question, answer) VALUES (?, ?, ?)",
        deck_id, question, answer
    )

    return redirect(f"/deck_view/{deck_id}")


@app.route("/import_deck", methods=["POST"])
@login_required
def import_deck():
    # You need deck_id to know where to import cards
    deck_id = request.form.get("deck_id")
    if not deck_id or not deck_id.isdigit():
        return apology("Missing or invalid deck id", 400)

    if "csv_deck" not in request.files:
        return apology("No file uploaded", 400)

    file = request.files["csv_deck"]
    if file.filename == '':
        return apology("No selected file", 400)

    if not file.filename.endswith('.csv'):
        return apology("Only CSV files allowed", 400)

    try:
        csv_file = TextIOWrapper(file.stream, encoding='utf-8')
        cards = csv.reader(csv_file)

        for card in cards:
            question, answer = card
            db.execute(
                "INSERT INTO cards (deck_id, question, answer) VALUES (?, ?, ?)",
                deck_id, question, answer
            )

        return redirect(f"/deck_view/{deck_id}")
    except Exception as e:
        return apology(f"Error importing deck: {str(e)}", 500)


@app.route("/delete_deck", methods=["POST"])
@login_required
def delete_deck():
    deck_id = request.form.get("deck_id")

    if not deck_id or not deck_id.isdigit():
        return apology("missing or invalid deck id", 400)

    db.execute(
        "DELETE FROM decks WHERE id = ? AND user_id = ?",
        deck_id, session["user_id"]
    )

    return redirect("/")


@app.route("/delete_card", methods=["POST"])
@login_required
def delete_card():
    card_id = request.form.get("card_id")

    if not card_id or not card_id.isdigit():
        return apology("missing or invalid card id", 400)

    deck_id_result = db.execute(
        """
        SELECT deck_id
        FROM cards
        WHERE id = ?
        """, card_id
    )

    if not deck_id_result:
        return apology("card not found", 404)

    deck_id = deck_id_result[0]["deck_id"]

    db.execute(
        "DELETE FROM cards WHERE id = ?",
        card_id
    )

    return redirect(f"/deck_view/{deck_id}")


@login_required
def get_deck_info(deck):
    deck["icon"] = deck_icons[deck["icon"]]

    cards_num = db.execute(
        """
        SELECT COUNT(*) AS cards_num
        FROM cards
        WHERE deck_id = ?
        """, deck["id"]
    )
    deck["cards_num"] = cards_num[0]["cards_num"] if cards_num else 0

    to_learn_num = db.execute(
        """
        SELECT COUNT(*) AS to_learn_num
        FROM progresses
        JOIN cards ON cards.id = progresses.card_id
        WHERE cards.deck_id = ?
        AND progresses.user_id = ?
        AND progresses.progress != 10
        """, deck["id"], session["user_id"]
    )
    deck["to_learn_num"] = to_learn_num[0]["to_learn_num"] if to_learn_num else 0


@app.route("/deck_view/<int:deck_id>")
@login_required
def deck_view(deck_id):
    cards = db.execute(
        """
        SELECT cards.id AS id, question, answer, progress
        FROM cards
        JOIN progresses ON progresses.card_id = cards.id
        WHERE deck_id = ?
        AND user_id = ?
        ORDER BY cards.id
        """, deck_id, session["user_id"])

    deck = db.execute(
        """
        SELECT id, name, color, icon
        FROM decks
        WHERE id = ?
        """, deck_id)[0]

    get_deck_info(deck)

    return render_template("deck_view.html", deck=deck, cards=cards, practice=True)


@app.route("/card_view/<int:card_id>")
@login_required
def card_view(card_id):
    card = db.execute(
        """
        SELECT cards.id AS id, question, answer, progress, deck_id
        FROM cards
        JOIN progresses ON progresses.card_id = cards.id
        WHERE cards.id = ?
        AND user_id = ?
        """, card_id, session["user_id"]
    )[0]

    if not card:
        return apology("card not found", 404)

    deck = db.execute(
        """
        SELECT id, name, color, icon
        FROM decks
        WHERE id = ?
        """, card["deck_id"]
    )[0]

    if not deck:
        return apology("deck not found", 404)

    get_deck_info(deck)

    return render_template("card_view.html", deck=deck, card=card)


@app.route("/update_card", methods=["POST"])
@login_required
def update_card():
    question = request.form.get("question")
    answer = request.form.get("answer")
    card_id = request.form.get("card_id")

    if not question or not answer or not card_id:
        return apology("missing data", 400)

    db.execute(
        "UPDATE cards SET question = ?, answer = ? WHERE id = ?",
        question, answer, card_id
    )

    deck_id = db.execute("SELECT deck_id FROM cards WHERE id = ?", card_id)[0]["deck_id"]

    return redirect(f"/deck_view/{deck_id}")


@app.route("/update_card_progress", methods=["POST"])
@login_required
def update_card_progress():
    card_id = request.form.get("card_id")
    response = int(request.form.get("response"))

    if card_id is None or response not in (0, 1):
        return jsonify({"error": "missing or invalid data"}), 400

    try:
        card_exists = db.execute("SELECT 1 FROM cards WHERE id = ?", card_id)
        if not card_exists:
            return jsonify({"error": "card does not exist"}), 400

        row = db.execute(
            "SELECT progress FROM progresses WHERE card_id = ? AND user_id = ?",
            card_id, session["user_id"]
        )
        progress = int(row[0]["progress"])

        if response == 1:
            progress += 1
        else:
            progress -= 1

        progress = max(0, min(10, progress))

        db.execute(
            "UPDATE progresses SET progress = ? WHERE card_id = ? AND user_id = ?",
            progress, card_id, session["user_id"]
        )

        return jsonify({"success": True, "progress": progress})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/practice", methods=["POST"])
@login_required
def practice():
    deck_id = request.form.get("deck_id")
    all_cards = request.form.get("all") == "1"
    practice_num = request.form.get("quantity")

    if not deck_id or not deck_id.isdigit():
        return apology("Invalid deck", 400)

    last_session = db.execute(
        "SELECT MAX(log_date) as last FROM sessions WHERE user_id = ?",
        session["user_id"]
    )[0]["last"]

    db.execute(
        "INSERT INTO sessions (user_id) VALUES (?)",
        session["user_id"]
    )

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    if last_session and datetime.datetime.strptime(last_session, "%Y-%m-%d %H:%M:%S").date() == yesterday:
        db.execute(
            "UPDATE users SET streak = streak + 1 WHERE id = ?", session["user_id"])
    elif last_session != today.isoformat():
        db.execute("UPDATE users SET streak = 1 WHERE id = ?",
                   session["user_id"])


    cards = db.execute(
        """
        SELECT cards.id AS id, question, answer, progress
        FROM cards
        JOIN progresses ON progresses.card_id = cards.id
        WHERE deck_id = ?
        AND user_id = ?
        """, deck_id, session["user_id"]
    )

    if all_cards:
        practice_num = len(cards)

    if not cards:
        return apology("No cards to practice", 400)

    deck = db.execute(
        """
        SELECT id, name, color, icon
        FROM decks
        WHERE id = ?
        """, deck_id
    )[0]
    get_deck_info(deck)

    try:
        practice_num = int(practice_num)
    except (TypeError, ValueError):
        return apology("Invalid number of cards", 400)

    if practice_num > len(cards):
        return apology("Not enough cards", 400)

    cards = random.sample(cards, practice_num)
    deck["practice_num"] = practice_num

    if not deck:
        return apology("deck not found", 404)

    return render_template("practice.html", cards=cards, deck=deck)


@app.route("/update_profile_pic", methods=["POST"])
@login_required
def update_profile_pic():
    profile_pic_id = request.form.get("profile_pic_id")

    if not profile_pic_id:
        return apology("missing data", 400)

    db.execute(
        "UPDATE users SET profile_pic_id = ? WHERE id = ?",
        profile_pic_id, session["user_id"]
    )

    return redirect("/settings")


@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return apology("missing data", 400)

    db.execute(
        "UPDATE users SET username = ?, hash = ? WHERE id = ?",
        username, generate_password_hash(password), session["user_id"]
    )

    return redirect("/settings")

@app.route("/", methods=["GET"])
def index():
    if "user_id" in session:
        decks = db.execute(
            """
            SELECT id, name, color, icon
            FROM decks
            WHERE user_id = ?
            """, session["user_id"])

        for deck in decks:
            get_deck_info(deck)
        return render_template("home.html", decks=decks, home=True)
    else:
        return render_template("landing.html")

@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
    session.clear()
    return redirect("/")