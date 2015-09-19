import lxml.html
import requests
from unidecode import unidecode
import time
import random
import datetime
import json
import os
import pickle
from models import *
from text_classify import algorithms
from textblob import TextBlob
from tools import * #ParsePhoneNumber, ParseAddress
from app import db
phone_parser = ParsePhoneNumber()

#a web scraper, for local computation
#At present, this seems to work fine
class Scraper:
    def __init__(self,place=None,investigation=None):
        if place:
            self.base_urls = self.map_place(place)
        else:
            self.base_urls = [
                "http://newyork.backpage.com/FemaleEscorts/",
                "http://newyork.backpage.com/BodyRubs/",
                "http://newyork.backpage.com/Strippers/",
                "http://newyork.backpage.com/Domination/",
                "http://newyork.backpage.com/TranssexualEscorts/",
                "http://newyork.backpage.com/MaleEscorts/",
                "http://newyork.backpage.com/Datelines/",
                "http://newyork.backpage.com/AdultJobs/"
            ]
        if investigation:
            self.investigation = investigation
    
    def update_investigation(self,investigation):
        self.investigation = investigation
    
    def update_place(self,place):
        self.base_urls = self.map_place(place)

    #ToDo, iterate to pages further back in time.
    #fine for now
    def generate_pages(self,url):
        urls = []
        endings = [
            "FemaleEscorts/",
            "BodyRubs/",
            "Strippers/",
            "Domination/",
            "TranssexualEscorts/",
            "MaleEscorts/",
            "Datelines/",
            "AdultJobs/"
        ]
        init_urls = []
        for ending in endings:
            init_urls.append(url+ending)
        for i in xrange(1,6):
            for url in init_urls:
                urls.append(url+"?page="+str(i))
        urls = init_urls + urls
        return urls
    
    #fine
    def map_place(self,place):
        #I believe this is lazy evaluation, otherwise, I'm kinda dumb...
        places = {
            "alabama":self.generate_pages("http://alabama.backpage.com/"),
            "manhattan":self.generate_pages("http://manhattan.backpage.com/"),
            "new york":self.generate_pages("http://newyork.backpage.com/"),
            "new york city":self.generate_pages("http://manhattan.backpage.com/")+self.generate_pages("http://statenisland.backpage.com/")+self.generate_pages("http://queens.backpage.com/")+self.generate_pages("http://brooklyn.backpage.com/")+self.generate_pages("http://bronx.backpage.com/"),
            "buffalo":self.generate_pages("http://buffalo.backpage.com/"),
            "albany new york":self.generate_pages("http://albany.backpage.com/"),
            "binghamton":self.generate_pages("http://binghamton.backpage.com/"),
            "catskills":self.generate_pages("http://catskills.backpage.com/"),
            "chautauqua":self.generate_pages("http://chautauqua.backpage.com/"),
            "elmira":self.generate_pages("http://elmira.backpage.com/"),
            "fairfield":self.generate_pages("http://fairfield.backpage.com/"),
            "fingerlakes":self.generate_pages("http://fingerlakes.backpage.com/"),
            "glens falls":self.generate_pages("http://glensfalls.backpage.com/"),
            "hudson valley":self.generate_pages("http://hudsonvalley.backpage.com/"),
            "ithaca":self.generate_pages("http://ithaca.backpage.com/"),
            "long island":self.generate_pages("http://longisland.backpage.com/"),
            "oneonta":self.generate_pages("http://oneonta.backpage.com/"),
            "plattsburgh":self.generate_pages("http://plattsburgh.backpage.com/"),
            "potsdam":self.generate_pages("http://plattsburgh.backpage.com/"),
            "rochester":self.generate_pages("http://plattsburgh.backpage.com/"),
            "syracuse":self.generate_pages("http://plattsburgh.backpage.com/"),
            "twintiers":self.generate_pages("http://twintiers.backpage.com/"),
            "utica":self.generate_pages("http://utica.backpage.com/"),
            "watertown":self.generate_pages("http://watertown.backpage.com/"),
            "westchester":self.generate_pages("http://watertown.backpage.com/")
        }
        return places[place]
        
    #need to add TfIdf
    #need to merge investigate and scrape methods or split this up further in someway, but currently this is bad and confusing
    def investigate(self):
        data = self.scrape(self.base_urls)
        training_data = [(elem, "trafficking") for elem in BackpageLogger.query.filter_by(is_trafficking=True).all()] 
        training_data = [(elem, "not trafficking") for elem in BackpageLogger.query.filter_by(is_trafficking=False).all()]
        cls = []
        cls.append(algorithms.svm(train))
        cls.append(algorithms.decision_tree(train))
        nb = algorithms.naive_bayes(train)
        for datum in data:
            if len(train) > 50: #totally a hack/rule of thumb 
                for cl in cls:
                    if cl.classify(algorithms.preprocess(datum["text_body"])) == "trafficking":
                        self.save_ads([datum])
            else:
                if nb.classify(datum["text_body"]) == 'trafficking':
                    self.save_ads([datum])
        time.sleep(700) # wait ~ 12 minutes (consider changing this)
        self.investigate() #this is an infinite loop, which I am okay with.

    #Todos:
    #add location data and pull that in
    def scrape(self,links=[],ads=True,translator=False):
        responses = []
        values = {}
        data = []
        
        if ads:
            for link in links:
                r = requests.get(link)
                responses.append(r)
        else:
            for link in links:
                r = requests.get(link)
                text = unidecode(r.text)
                html = lxml.html.fromstring(text)

                links = html.xpath("//div[@class='cat']/a/@href")
                for link in links:
                    #consider changing this...since we probably won't have that many base_urls but will be scraping a bunch of times
                    #It should really be something having to do with a counter..
                    if len(self.base_urls) > 1 or len(self.base_urls[0]) > 3:
                        time.sleep(random.randint(5,27))
                    try:
                        responses.append(requests.get(link))
                        print link
                    except requests.exceptions.ConnectionError:
                        print "hitting connection error"
                        continue
        return responses
    
    def save(responses,investigation="default"):
        for r in responses:
            text = r.text
            html = lxml.html.fromstring(text)
            #getting address information from html page
            addr_parser = ParseAddress()
            possible_locations = html.xpath('//div[@style="padding-left:2em;"]')
            potential_lat_longs = []
            for loc in possible_locations:
                if "Location" in loc.text_content():
                    for possible in loc.text_content().split("Location:")[1].split(","):
                        potential_lat_longs.append(addr_parser.parse(possible))
            lat_longs = [elem for elem in potential_lat_longs if elem != None]
            for lat_long in lat_longs:
                addr_log = AddressLogger(lat=lat_long.latitude,long=lat_long.longitude)
                db.session.add(addr_log)
                db.session.commit()
            values["title"] = html.xpath("//div[@id='postingTitle']/a/h1")[0].text_content()
            values["link"] = unidecode(r.url)
            # Stub - add this with textRank - values["new_keywords"] = []
            try:
                values["images"] = html.xpath("//img/@src")
            except IndexError:
                values["images"] = "weird index error"
            pre_decode_text = html.xpath("//div[@class='postingBody']")[0].text_content().replace("\n","").replace("\r","")  
            values["text_body"] = pre_decode_text 
            try:
                values["posted_at"] = html.xpath("//div[class='adInfo']")[0].text_content().replace("\n"," ").replace("\r","")
            except IndexError:
                values["posted_at"] = "not given"
            values["scraped_at"] = str(datetime.datetime.now())
            body_blob = TextBlob(values["text_body"])
            title_blob = TextBlob(values["title"])
            values["language"] = body_blob.detect_language() #requires the internet - makes use of google translate api
            values["polarity"] = body_blob.polarity
            values["subjectivity"] = body_blob.sentiment[1]
            if values["language"] != "en" and not translator:
                values["translated_body"] = body_blob.translate(from_lang="es")
                values["translated_title"] = title_blob.translate(from_lang="es")
            else:
                values["translated_body"] = "none"
                values["translated_title"] = "none"
            text_body = values["text_body"]
            title = values["title"]
            values["phone_numbers"] = phone_parser.phone_number_parse(values)
            #is_trafficking is currently missing because it is being handled in investigate for some reason
            #this needs to be added to this method/made more readible
            for p_number in values['phone_numbers']:
                ad_phone_number = PhoneNumberLogger(p_number)
                db.session.add(ad_phone_number)
                db.session.commit()

            bp_ad = BackpageLogger(
                text_body=values["text_body"],
                text_headline=values["title"],
                investigation=investigation,
                link=values['link'],
                photos=values['photos'],
                language=values['language'],
                polarity=values['polarity'],
                translated_body=values['translated_body'],
                translated_title=values['translated_title'],
                subjectivity=values['subjectivity'],
                posted_at=values['posted_at'],
                phone_number=json.dumps(values['phone_numbers'])#this is gross and will be fixed at some point
            )
            db.session.add(bp_ad)
            db.session.commit()
            data.append(values)
        return data

    #should this method remain?
    def initial_scrape(self,links):
        responses = self.scrape(links)
        data = self.save(responses)
        return data

if __name__ == '__main__':
    scraper = Scraper(place="new york")
    data = scraper.initial_scrape(links=["http://newyork.backpage.com/FemaleEscorts/"])
    print data
    
    
