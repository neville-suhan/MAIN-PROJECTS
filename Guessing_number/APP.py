from flask import Flask, render_template, request, redirect, url_for, session, flash
from game_logic import GameLogic
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session handling

USERS_FILE = "users.txt"

# Ensure users.txt exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        pass


# ---------------- AUTH HELPERS ----------------
def authenticate_user(username, password):
    with open(USERS_FILE, "r") as f:
        for line in f:
            stored_user, stored_pass = line.strip().split(",")
            if stored_user == username and stored_pass == password:
                return True
    return False

def register_user(username, password):
    with open(USERS_FILE, "r") as f:
        for line in f:
            stored_user, _ = line.strip().split(",")
            if stored_user == username:
                return False
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")
    return True


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if authenticate_user(username, password):
            session["username"] = username
            session["game"] = GameLogic().__dict__  # save game state
            return redirect(url_for("game"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if username and password:
            if register_user(username, password):
                flash("Account created! Please login.", "success")
                return redirect(url_for("login"))
            else:
                flash("Username already exists!", "danger")
        else:
            flash("Please fill all fields!", "danger")
    return render_template("signup.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    if "username" not in session:
        return redirect(url_for("login"))

    # restore game state
    game_state = GameLogic()
    game_state.__dict__ = session.get("game", game_state.__dict__)

    message = ""
    hint = ""

    if request.method == "POST":
        if "guess" in request.form:
            try:
                guess = int(request.form["guess"])
                message = game_state.check_guess(guess)
                if message == "Correct!":
                    flash(f"🎉 You guessed it in {game_state.attempts} tries!", "success")
                    game_state.reset_game()
            except ValueError:
                message = "⚠️ Please enter a valid number!"
        elif "hint" in request.form:
            hint = game_state.get_hint()
        elif "quit" in request.form:
            answer = game_state.reveal_answer()
            flash(f"Game Over! The correct number was {answer}", "info")
            game_state.reset_game()

    # save state back to session
    session["game"] = game_state.__dict__

    return render_template("game.html", username=session["username"], message=message, hint=hint)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True,port=5001)
