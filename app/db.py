
import sqlite3
import copy

dbpath = "db.db"

def __reset():
    """Wipes the entire database file, creates the table.
Returns nothing."""
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS blog_posts")
    c.execute("CREATE TABLE users (uuid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password BLOB)")
    c.execute("CREATE TABLE blog_posts (pid INTEGER PRIMARY KEY AUTOINCREMENT, owner INTEGER, title TEXT, contents BLOB, published INTEGER)")
    c.execute("CREATE TABLE user_likes (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid INTEGER, pid INTEGER)")
    db.commit()

def setup_db():
    # Create tables only when missing, without deleting saved posts.
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (uuid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password BLOB)")
    c.execute("CREATE TABLE IF NOT EXISTS blog_posts (pid INTEGER PRIMARY KEY AUTOINCREMENT, owner INTEGER, title TEXT, contents BLOB, published INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS user_likes (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid INTEGER, pid INTEGER)")
    db.commit()
    db.close()

def _check_liked(c, uuid: int, pid: int):
    c.execute(f"SELECT EXISTS(SELECT 1 FROM user_likes WHERE uuid = {uuid} AND pid = {pid});")
    return c.fetchone()[0] != 0

def like_post(uuid: int, pid: int):
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    if _check_liked(c, uuid, pid):
        c.execute(f"DELETE FROM user_likes WHERE uuid = {uuid} AND pid = {pid};")
        r = 0
    else:
        c.execute(f"INSERT INTO user_likes (uuid, pid) VALUES ({uuid}, {pid})")
        r = 1
    db.commit()
    db.close()
    return r

def count_likes(pid: int):
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute(f"SELECT COUNT(*) FROM user_likes WHERE pid = {pid}")
    return c.fetchone()[0]

def __turn_cursor_into_list(table:str, c):
    header = ["uuid", "username", "password"] if table == "users" else ['pid', 'owner', 'title', 'contents', 'published']

    result = []
    contents = [a for a in c]
    for user in contents:
        d = {}
        for i, key in enumerate(header):
            d[key] = user[i]
        result.append(copy.deepcopy(d))
    return result

def add_user(name:str, password=None):
    """Adds a new user to the database.
Returns nothing.

name -- username that the user is gonna have
password -- the user's password, unencrypted.

e.g. add_user("pig")
e.g. add_user("john_dont", "pass123secret")"""
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    if password:
        c.execute(f"INSERT INTO users (username, password) VALUES ('{name}', '{password}')")
    else:
        c.execute(f"INSERT INTO users (username) VALUES ('{name}')")
    db.commit()

def add_blog(owner:int, title:str, contents, published=False):
    """Add a blog post to database"""
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute(
        "INSERT INTO blog_posts (owner, title, contents, published) VALUES (?, ?, ?, ?)",
        (owner, title, contents, 1 if published else 0)
    )
    db.commit()
    db.close()

def get_user(key):
    """Gets user from the database.

key -- either the uuid or username of the user."""
    return __get_user_or_blog(key, "users")

def get_blog(key):
    if (type(key) == str):
        key = key.replace("'", "''")
    return __get_user_or_blog(key, "blog_posts")

def get_blog_by_pid(pid: int) -> dict:
    """IMPORTANT DOES NOT RETURN A LIST BECAUSE PID ARE PRIMARY KEY"""
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute(f"SELECT * FROM blog_posts WHERE pid = {pid}")
    return __turn_cursor_into_list("blog_posts", c)[0]

def edit_blog(pid: int, title: str, contents, published):
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute(f'UPDATE blog_posts SET title = "{title}", contents = "{contents}", published = {published} WHERE pid = {pid}')
    db.commit()
    db.close()

def get_blogs(user: str | int, start: int, end: int):
    db = sqlite3.connect(dbpath)
    c = db.cursor()

    if isinstance(user, int):
        uuid = user
    elif isinstance(user, str):
        u = get_user(user)
        if u is None or len(u) == 0:
            return []
        uuid = u[0]["uuid"]

    c.execute(f"SELECT * FROM blog_posts WHERE owner = {uuid} LIMIT {end - start} OFFSET {start}")
    return __turn_cursor_into_list("blog_posts", c)

def __get_user_or_blog(key, which:str):
    """get_user(-) and get_blog(-) are wrappers of this method.

which -- "users" or "blog_posts"."""
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    try:
        # Choose which column to search.
        by = ('username' if type(key) == str else 'uuid') if which == "users" else ('title' if type(key) == str else 'owner')
        c.execute(f"SELECT * FROM {which} WHERE {by} = '{key}'")
        d = __turn_cursor_into_list(which, c)
        return d
    except:
        return None
    
def select(table:str, query:str):
    """Runs the SQLite3 query on the cursor exactly, returns a list of dictionaries based on what is selected.
    This function exists if something more specific needs to be done.
    Note that this query must be a SELECT query for it to work properly.
    query -- The SQLite3 query.
    table -- The table you are acting upon.
    """
    db = sqlite3.connect(dbpath)
    c = db.cursor()
    c.execute(query)
    return __turn_cursor_into_list(table, c)

if __name__ == '__main__':
    print(like_post(1, 22))
    print(like_post(2, 22))
    print(like_post(3, 22))
    print(count_likes(22))