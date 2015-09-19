from flask import render_template,redirect,request,url_for
from app import app
import pickle
from crawler import Scraper
from multiprocessing import Process

scraper = Scraper()
investigate = Process(target=scraper.investigate)
investigate.daemon=True

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

#Data Visualization Routes
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

#Web Scraping Routes
@app.route("/webscraping",methods=["GET","POST"])
def webscraping():
    return render_template("webscraping.html")

@app.route("/run",methods=["GET","POST"])
def run():
    data = scraper.scrape(links=["http://www.backpage.com"])
    return redirect(url_for("webscraping"))

@app.route("/investigate",methods=["GET","POST"])
def investigator():
    if request.method == "POST":
        place = request.form.get("place")
        scraper.update_place(place)
        investigate.start()
    return redirect(url_for("webscraping"))

@app.route("/stop_investigation",methods=["GET","POST"])
def stop_investigation():
    #semantic bug here, fix this later (create a thread pool)
    investigate.terminate()
    return redirect(url_for("webscraping"))

@app.route("/add",methods=["GET","POST"])
def add():
    return render_template("add.html")

@app.route("/add_data",methods=["GET","POST"])
def add_data():
    if request.method=="POST":
        investigation_type = request.form.get("investigation_type")
        url = request.form.get("url_list")
        urls = url.split(",")
        print scraper.initial_scrape(links=urls)
        scraper.update_investigation(urls)
    return redirect(url_for("webscraping"))
