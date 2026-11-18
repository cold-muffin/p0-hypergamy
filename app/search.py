from flask import Flask
from flask import render_template
from flask import request
from db import get_user, select

def search():
    query = request.args.get("query", '')
    results = select("users", f"SELECT * FROM users WHERE username LIKE '%{query}%'")
    return render_template("search.html", query = query, results = results)
