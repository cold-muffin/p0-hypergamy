import sqlite3
import copy

dbpath = "db.db"
db = sqlite3.connect(dbpath)
c = db.cursor()

def __reset():
    """Wipes the entire database file, creates the table.\nReturns nothing."""
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS blog_posts")
    c.execute("CREATE TABLE users (uuid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password BLOB)")
    c.execute("CREATE TABLE blog_posts (pid INTEGER PRIMARY KEY AUTOINCREMENT, owner INTEGER, title TEXT, contents BLOB, published INTEGER)")
    db.commit()
    
def __turn_cursor_into_list(table:str):
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
    """Adds a new user to the database.\nReturns nothing.\n\nname -- username that the user is gonna have password -- the user's password, unencrypted. NOTE that at the moment, this function does not encrypt the password. Oops! (default=None)\n\ne.g. add_user("pig")\ne.g. add_user("john_dont", "pass123secret")"""
    if password:
        c.execute(f"INSERT INTO users (username, password) VALUES ('{name}', '{password}')")
    else:
        c.execute(f"INSERT INTO users (username) VALUES ('{name}')")
    db.commit()
    
def add_blog(owner:int, title:str, contents, published=False):
    title = title.replace("'", "''")
    """Adds a new blog post to the database.\nReturns nothing.\n\nowner (int) -- uuid of the blog post's owner\ntitle (str) -- title of the blog post\ncontents -- contents of the file, in whatever data\n* published (boolean) -- if the blog post is public or not (default=False)"""
    c.execute(f"INSERT INTO blog_posts (owner, title, contents, published) VALUES ({owner}, '{title}', {contents}, {1 if published else 0});")
    db.commit()

def get_user(key):
    """Gets user from the database. You cannot select a user by the password.\nReturns a dictionary with the user's data. or returns None if there is an error.\n\nkey -- either the uuid or the username of the user you want to retrieve.\n\ne.g. get_user(3) -> {'uuid': 3, 'username': 'john_doe', 'password': 'pass123secret'}\ne.g. get_user("john_doe") -> {'uuid': 3, 'username': 'john_doe', 'password': 'pass123secret'}"""
    return __get_user_or_blog(key, "users")

def get_blog(key):
    """Gets the blog that matches the given pid.\nkey : int = gets the blog post by the pid."""
    return __get_user_or_blog(key, "blog_posts")[0]

def get_all_user_posts(key):
    """Gets all blog posts that a specific user made.\n\nkey -- either the username (str) or the uuid (int) of the user whom you are trying to get posts from."""
    return __get_user_or_blog(key, "users")
        
def __get_user_or_blog(key, which:str):
    """get_user(-) and get_blog(-) are wrappers of this method.\n\nwhich -- which db you want. Only valid values are "users" or "blog_posts"."""
    try:
        # this line: decides which column names to use depending on the db u want.
        by = ('username' if type(key) == str else 'uuid') if which == "users" else ('pid')
        c.execute(f"SELECT * FROM {which} WHERE {by} = '{key}'")
        d = __turn_cursor_into_list(which)
        return d
    except:
        return None

if __name__ == '__main__':
    pass