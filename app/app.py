from flask import Flask
from flask import render_template
from search import search
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from db import add_user, get_user, get_blog, setup_db
from auth import auth, auth_signup

app = Flask(__name__)
app.secret_key = "dev"
setup_db()  # Make tables if they do not already exist

@app.route("/")
def root():
    return render_template("response.html", username = session.get("username"))

@app.route("/login")
def login():
    error = request.args.get('error')
    return render_template("login.html", error=error)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username")
    return render_template("logout.html")

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
    error = request.args.get("error")
    return render_template("new_user.html", error=error)

@app.route("/create_user", methods=["POST"])
def create_user():
    user = request.form.get("username")
    password = request.form.get("password")
    a = auth_signup(user, password)
    if a[0]:
        return redirect("/login")

    return redirect(url_for("new_user", error=a[1]))

@app.route("/search")
def search_h():
    return search()

@app.route("/profile")
def profile():
    #User's own profile
    username = session.get("username")
    if not username:
        return redirect("/login")

    users = get_user(username)
    if not users:
        return redirect("/login")

    return redirect("/profiles/" + str(users[0]["uuid"]))


@app.route("/profiles/<int:user_id>")
def view_profile(user_id):
    users = get_user(user_id)
    if not users:
        return "User not found", 404

    user = users[0]
    is_owner = session.get("username") == user["username"]
    posts = get_blog(user_id) or []

    # Only the owner can see unpublished posts
    if not is_owner:
        posts = [post for post in posts if post["published"]]

    # Newest posts first
    posts.sort(key=lambda post: post["pid"], reverse=True)

    # Contents may be saved as bytes in the database.
    for post in posts:
        if isinstance(post["contents"], bytes):
            post["contents"] = post["contents"].decode("utf-8", errors="replace")

    return render_template("profile.html", user=user, posts=posts, is_owner=is_owner)


if __name__ == "__main__":
    app.run(debug=True)
