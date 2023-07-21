import os, json, datetime, shutil, sys
from flask import Flask, request, jsonify, send_from_directory, render_template, flash, redirect, url_for, send_file
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from models import *

app = Flask(__name__)
CORS(app)

data = {}

if not os.path.isfile(os.path.join(os.getcwd(), "data.txt")):
    with open("data.txt", "w") as f:
        json.dump({
            "loggedInToken": None,
            "questions": {}
        }, f)
        data = {
            "loggedInToken": None,
            "questions": {}
        }
else:
    with open("data.txt", "r") as f:
        data = json.load(f)

@app.route("/")
def homepage():
    return render_template("index.html")

## Import routes declared from services
from assets import *

from api import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)