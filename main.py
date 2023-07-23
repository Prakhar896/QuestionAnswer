import os, json, datetime, shutil, sys, copy
from flask import Flask, request, jsonify, send_from_directory, render_template, flash, redirect, url_for, send_file
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from models import *

app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET_KEY"]
CORS(app)

data = {}

if not os.path.isfile(os.path.join(os.getcwd(), "data.txt")):
    with open("data.txt", "w") as f:
        json.dump({
            "loggedInToken": None,
            "session": {
                "active": False,
                "activationDatetime": "Not Available"
            },
            "questions": {}
        }, f)
        data = {
            "loggedInToken": None,
            "session": {
                "active": False,
                "activationDatetime": "Not Available"
            },
            "questions": {}
        }
else:
    with open("data.txt", "r") as f:
        data = json.load(f)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/ask")
def ask():
    return render_template("ask.html")

@app.route("/logout")
def logout():
    if 'token' not in request.args:
        flash("Token not present in request.")
        return redirect(url_for("error"))
    if request.args['token'] != data['loggedInToken']:
        flash("Invalid token.")
        return redirect(url_for("error"))
    
    data['loggedInToken'] = None
    saveToFile(data)
    return redirect(url_for("homepage"))

@app.route("/security/unauthorised")
def unauthorised():
    return render_template("unauthorised.html")

@app.route("/security/error")
def error():
    if 'error' not in request.args:
        return render_template('error.html', error=None)
    else:
        return render_template('error.html', error=request.args['error'])

## Import routes declared from services
from assets import *

from session import *

from api import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)