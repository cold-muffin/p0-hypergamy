from flask import Flask
from flask import render_template
from search import search
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from db import __reset, add_user
from auth import auth

app = Flask(__name__)
app.secret_key = "dev"

@app.route("/")
def root():
    return render_template("response.html", username = session.get("username"))

@app.route("/login")
def login():
    error = request.args.get('error')
    return render_template("login.html", error=error)

@app.route("/auth", methods=["POST"])
def authenticate():
    user = request.form.get("username")
    password = request.form.get("password")

    a = auth(user, password)
    print(a)
    if a[0]:
        session["username"] = user
        return redirect("/profile")
    
    return redirect(url_for("login", error=a[1]))

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
