# \<WeBlog\> by \<Hypergamy\>

**WeBlog** is a super awesome blog hosting and sharing site, where you can update your own blog and see blogs of other users. 

You can see other people's blogs without logging in to see what's happening on the site. To start creating your own blogs, you must register an account. 

## Install Guide

### 1. Clone Repository

```
git clone git@github.com:cold-muffin/p0-hypergamy.git # clone repo
cd p0-hypergamy # enter directory
```

### 2a. Quick n' dirty

May not work if your machine doesn't give you permission to install external libraries. Main python environment may also become dirty after this.

```
pip install -r requirements.txt # install dependencies
python app/serve.py # run app
```

### 2b. Clean

Takes a little longer but is significantly more organized. Make sure to choose a method of running the app.

```
python -m venv .venv # create virtual environment
source .venv/bin/activate
pip install -r requirements.txt # install dependencies
# Uncomment one of these lines:
# python app/serve.py # run app in prod mode
# python app/app.py # run app in dev mode
```

**NOTES**:
- Make sure your machine is authenticated to GitHub and is able to clone remote repositories
- Some machines may require calling `python3` instead of `python` to create the virtual environment
