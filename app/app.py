from flask import Flask
from flask import render_template
from search import search

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello world"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/search")
def search_h():
    return search()

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
