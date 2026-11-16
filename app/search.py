from flask import Flask
from flask import render_template
from flask import request

def search():
    query = request.args.get("query", '')
    return render_template("search.html", query = query)
