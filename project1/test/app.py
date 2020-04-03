import json
from flask import Flask, render_template,request


app = Flask(__name__)

@app.route("/")
def result():
  return render_template("test.html")

@app.route('/')
def get_data(chart_ID='chart'):
  labels = ["Africa", "Asia", "Europe", "Latin America", "North America"]
  data = [5578,5267,734,784,433]
  return flask.jsonify({'payload':json.dumps({'data':data, 'labels':labels})})