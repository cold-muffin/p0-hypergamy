from flask import Flask
from flask import render_template
from search import search
from flask import session
from flask import request
from flask import redirect

from db import __reset, add_user, get_user

app = Flask(__name__)
app.secret_key = "dev"

@app.route("/")
def root():
    return render_template("response.html", username = session.get("username"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def authenticate():
    user = request.form.get("username")
    password = request.form.get("password")

    if get_user(user)[0]["password"] == password:
        session["username"] = user
        return redirect("/profile")

    return "Failed"

@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    user = request.form.get("username")
    password = request.form.get("password")
    add_user(user, password)
    return redirect("/login")

@app.route("/search")
def search_h():
    return search()

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    __reset()
    app.run(debug=True)
