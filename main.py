import os, json, datetime, shutil, sys
from flask import Flask, request, jsonify, send_from_directory, render_template, flash, redirect, url_for, send_file
from flask_cors import CORS
from models import *

app = Flask(__name__)
CORS(app)

loggedInToken = None

@app.route("/")
def homepage():
    return render_template("index.html")

## Import routes declared from services
from assets import *

from api import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)