import requests
from flask import Flask, render_template
from flask_alchemy import SQLAlchemy

app = flask(__name__)

@app.route("/")
def index():
	return render_template('data.html')

