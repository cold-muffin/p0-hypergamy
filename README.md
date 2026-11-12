# \<WeBlog\> by \<Hypergamy\>

**WeBlog** is a super awesome blog hosting and sharing site, where you can update your own blog and see blogs of other users. 

You can see other people's blogs without logging in to see what's happening on the site. To start creating your own blogs, you must register an account. 

## Install Guide

### Quick n' dirty

```
git clone git@github.com:cold-muffin/p0-hypergamy.git # clone repo
pip install -r requirements.txt # install dependencies
python app/serve.py # run app
```

### Clean

```
git clone git@github.com:cold-muffin/p0-hypergamy.git # clone repo
python -m venv .venv # create virtual environment
pip install -r requirements.txt # install dependencies
# Uncomment one of these lines:
# python app/serve.py # run app in prod mode
# python app/app.py # run app in dev mode
```

**NOTES**:
- Make sure your machine is authenticated to GitHub and is able to clone remote repositories
- Some machines may require calling `python3` instead of `python` to create the virtual environment
