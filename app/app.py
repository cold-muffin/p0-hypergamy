from flask import Flask
from flask import render_template
from search import search
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from db import add_user, get_user, get_blog, setup_db, add_blog, get_blog_by_pid, edit_blog
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

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if "username" in session:
        session.pop("username")
    return render_template("logout.html")

@app.route("/auth", methods=["GET", "POST"])
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

@app.route("/create_user", methods=["GET", "POST"])
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
    #Navbar HTML to redirect to create post page
    if request.args.get("action") == "create":
        return redirect(url_for("create_post", user_id=users[0]["uuid"]))

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

@app.route("/profiles/<int:user_id>/edit/new")
def create_post(user_id):
    users = get_user(user_id)
    if users is None or len(users) == 0:
        return "User does not exist"
    user = users[0]

    # redirect to login if not logged in
    if "username" in session:
        is_owner = session["username"] == user["username"]
    else:
        return redirect(url_for("login"))

    return render_template("create_blog.html", user=user, is_owner=is_owner)

@app.route("/profiles/<int:user_id>/edit/<int:pid>")
def edit_post(user_id: int, pid: int):
    blog = get_blog_by_pid(pid)
    print(blog)

    users = get_user(user_id)
    if users is None or len(users) == 0:
        return "User does not exist"
    user = users[0]

    # redirect to login if not logged in
    if "username" in session:
        is_owner = session["username"] == user["username"]
    else:
        return redirect(url_for("login"))

    return render_template("edit_blog.html", user=user, is_owner=is_owner, post=blog)

@app.route("/publish_edit", methods=["GET", "POST"])
def publish_edit():
    # pid parsing
    pid = request.form.get("pid")
    if pid is None:
        return redirect(url_for("profile", error="POSTNOTFOUND"))
    pid = int(pid)

    # title parsing
    title = request.form.get("title")
    if title is None:
        return redirect(url_for("profile", error="NOTITLE"))

    # contents parsing
    contents = request.form.get("contents")

    # action parsing
    action = request.form.get("action")
    publish = action == "publish"
    if action is None:
        return redirect(url_for("profile", error="EARLYEXIT"))

    edit_blog(pid, title, contents, publish)
    # saving does not redirect you towards a different page
    post = get_blog_by_pid(pid)
    if action == "save":
        return redirect(url_for("edit_post", user_id=post["owner"], pid=pid))

    return redirect(url_for("profile"))

@app.route("/publish_post", methods=["GET", "POST"])
def publish_post():
    # uuid parsing
    uuid = request.form.get("uuid")
    if uuid is None:
        return redirect(url_for("profile", error="USERNOTFOUND"))
    uuid = int(uuid)

    # title parsing
    title = request.form.get("title")
    if title is None:
        return redirect(url_for("profile", error="NOTITLE"))
        
    # contents parsing
    contents = request.form.get("contents")

    # action parsing
    action = request.form.get("action")
    publish = action == "publish"

    if action is None:
        return redirect(url_for("profile", error="EARLYEXIT"))

    add_blog(uuid, title, contents, publish)

    print(request.form)
    return redirect(url_for("profile"))

@app.route("/toggle_like", methods=["GET", "POST"])
def like_post():
    pid = request.args.get("pid")
    uuid = request.args.get("uuid")
    return redirect(url_for("view_profile", user_id=uuid, _anchor=f"post-{pid}"))

if __name__ == "__main__":
    app.run(debug=True)
