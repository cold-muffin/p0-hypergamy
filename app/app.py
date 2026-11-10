from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello world"

@app.route("/login")
def login():
    return "Login"

@app.route("/new_user")
def new_user():
    return "New user"

@app.route("/search")
def search():
    return "Search"

if __name__ == "__main__":
    app.run(debug=True)
