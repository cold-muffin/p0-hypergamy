import sqlite3
import copy

dbpath = "db.db"
db = sqlite3.connect(dbpath)
c = db.cursor()

def __reset():
    """
    Wipes the entire database file, creates the table.
    Returns nothing.
    """
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS blog_posts")
    c.execute("CREATE TABLE users (uuid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password BLOB)")
    c.execute("CREATE TABLE blog_posts (pid INTEGER PRIMARY KEY AUTOINCREMENT, owner INTEGER, title TEXT, contents BLOB, published INTEGER)")
    db.commit()
    
def __turn_cursor_into_list(table:str):
    header = ["uuid", "username", "password"] if table == "users" else ['pid', 'owner', 'title', 'contents', 'published']
    
    result = []
    contents = [a for a in c]
    print(contents)
    for row in contents:
        d = {}
        for i, key in enumerate(header):
            d[key] = contents[i]
        result.append(copy.deepcopy(d))
    return result
        
def add_user(name, password=None):
    """
    Adds a new user to the database.
    Returns nothing.
    
    name -- username that the user is gonna have
    password -- the user's password, unencrypted. NOTE that at the moment, this function does not encrypt the password. Oops! (default=None)
    
    e.g. add_user("pig")
    e.g. add_user("john_dont", "pass123secret")
    """
    if password:
        c.execute(f"INSERT INTO users (username, password) VALUES ('{name}', '{password}')")
    else:
        c.execute(f"INSERT INTO users (username) VALUES ('{name}')")
    db.commit()
    
def get_user(key):
    """
    Gets user from the database. You cannot select a user by the password.
    Returns a dictionary with the user's data. or returns None if there is an error.
    
    key -- either the uuid or the username of the user you want to retrieve.
    
    e.g. get_user(3) -> {'uuid': 3, 'username': 'john_doe', 'password': 'pass123secret'}
    e.g. get_user("john_doe") -> {'uuid': 3, 'username': 'john_doe', 'password': 'pass123secret'}
    """
    d = {}
    
    try:
        by = 'username' if type(key) == str else 'uuid'
        c.execute(f"SELECT * FROM users WHERE {by} = '{key}'")
#         contents = [a for a in [a for a in c][0]]
#         d["uuid"] = contents[0]
#         d["username"] = contents[1]
#         d["password"] = contents[2]
        d = __turn_cursor_into_list("users")
        return d
    except:
        return None

if __name__ == '__main__':
    pass