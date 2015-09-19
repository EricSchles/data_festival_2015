import lxml.html
import requests
from unidecode import unidecode
import time
import random
import datetime
import json
import os
import pickle
from models import CRUD,Ads,TrainData,KeyWords
from text_classify import algorithms


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
        

    #need to fix
    def investigate(self):
        data = self.scrape(self.base_urls)
        train_crud = CRUD("sqlite:///database.db",Ads,"ads")
        #getting dummy data from http://www.dummytextgenerator.com/#jump
        dummy_crud = CRUD("sqlite:///database.db",TrainData,"training_data")
        train = train_crud.get_all()
        dummy = dummy_crud.get_all()
        t_docs = [elem.text for elem in train_crud.get_all()] #all documents with trafficking
        train = [(elem.text,"trafficking") for elem in train] + [(elem.text,"not trafficking") for elem in dummy]
        cls = []
        cls.append(algorithms.svm(train))
        cls.append(algorithms.decision_tree(train))
        for datum in data:
            for cl in cls:
                if cl.classify(algorithms.preprocess(datum["text_body"])) == "trafficking":
                    self.save_ads([datum])
            #so I don't have to eye ball things
            if doc_comparison(datum["text_body"],t_docs) == "trafficking":
                self.save_ads([datum])
                if self.doc_comparison(datum["text_body"],t_docs) == "trafficking":
                    self.save_ads([datum])

            #so I don't have to eye ball things
            if doc_comparison(datum["text_body"],t_docs) == "trafficking":
                self.save_ads([datum])

                if self.doc_comparison(datum["text_body"],t_docs) == "trafficking":
                    self.save_ads([datum])

        time.sleep(700) # wait ~ 12 minutes
        self.investigate() #this is an infinite loop, which I am okay with.
                    
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

        for r in responses:
            text = r.text
            html = lxml.html.fromstring(text)
            values["title"] = html.xpath("//div[@id='postingTitle']/a/h1")[0].text_content()
            values["link"] = unidecode(r.url)
            values["new_keywords"] = []
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
            values["phone_numbers"] = self.phone_number_parse(values)
            data.append(values)
        
        return data

    def initial_scrape(self,links):
        data = self.scrape(links)
        self.save_ads(data)
        return data
    
    def pull_keywords(self,text):
        """This method should remove any very common english words like 
        the, and and other statistically common words for english language"""
        pass

    def save_ads(self,data):
        crud = CRUD("sqlite:///database.db",table="ads")
        
        for datum in data:
            ad = Ads()
            ad.title=datum["title"]
            ad.phone_numbers=json.dumps(datum["phone_numbers"])
            ad.text_body=datum["text_body"]
            ad.photos=json.dumps(datum["images"])#change this so I'm saving actual pictures to the database.
            ad.link=datum["link"]
            ad.posted_at = datum["posted_at"]
            ad.scraped_at=datum["scraped_at"]
            ad.language=datum["language"]
            ad.polarity=datum["polarity"]
            ad.translated_body=datum["translated_body"]
            ad.translated_title=datum["translated_title"]
            ad.subjectivity=datum["subjectivity"]
            crud.insert(ad)
        
if __name__ == '__main__':
    scraper = Scraper(place="new york")
    data = scraper.initial_scrape(links=["http://newyork.backpage.com/FemaleEscorts/"])
    print data
    
    
