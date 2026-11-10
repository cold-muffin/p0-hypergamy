import sqlite3
import copy

db = sqlite3.connect("db.db")
c = db.cursor()

def __reset(path:str):
    """
    Wipes the entire database file. Initializes the tables.
    """
    f = open(path, mode='w')
    f.write('')
    f.close()

    c.execute("CREATE TABLE users (uuid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password BLOB)")
    c.execute("CREATE TABLE blog_posts (pid INTEGER PRIMARY KEY AUTOINCREMENT, owner INTEGER, title TEXT, contents BLOB, published INTEGER)")
    db.commit()
    
def get_user(key, by:str):
    """
    Gets user from the database. key is what you are using to select the user. by is a hint to tell
    what column you are selecting for.
    e.g. get_user("john_doe", "username")
    e.g. get_user(3, "uuid")
    """
    d = {}
    
    c.execute(f"SELECT * FROM users WHERE {by} = {key}")
    
if __name__ == '__main__':
    pass