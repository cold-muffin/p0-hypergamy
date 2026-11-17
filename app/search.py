#from flask import Flask
#from flask import render_template
#from flask import request
from db import get_user

def search():
    query = request.args.get("query", '')
    print(get_user(query))
    #return render_template("search.html", query = query, results = get_user(query))
