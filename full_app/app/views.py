from flask import render_template
from app import app

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/map", methods=["GET","POST"])
def map():
    return render_template("map.html")

@app.route("/timeseries",methods=["GET","POST"])
def timeseries():
    return render_template("timeseries.html")

@app.route("/bar",methods=["GET","POST"])
def bar():
    return render_template("bar.html")

@app.route("/pie",methods=["GET","POST"])
def pie():
    return render_template("pie.html")

