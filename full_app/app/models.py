from app import db
import datetime

class IPLogger(db.Model):
    __tablename__ = 'ip_logger'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self,ip_address):
        self.ip_address = ip_address 

    def __repr__(self):
        return '<ip_addr %r>' % self.ip_address

class PhoneNumberLogger(db.Model):
    __tablename__ = 'phone_number_logger'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self,phone_number):
        self.phone_number = phone_number
    
    def __repr__(self):
        return '<phone_number %r>' % self.phone_number

class AddressLogger(db.Model):
    __tablename__ = 'address_logger'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self,address):
        self.address = address

    def __repr(self):
        return '<address %r>' % self.address

class BackpageLogger(db.Model):
    __tablename__ = 'backpage_logger'
    id = db.Column(db.Integer, primary_key=True)
    text_body = db.Column(db.String(4000))
    text_headline = db.Column(db.String(4000))
    investigation = db.Column(db.String(1000))
    link = db.Column(db.String(10000))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    photos = db.Column(db.String(10000))
    language = db.Column(db.String(1000))
    polarity = db.Column(db.Float(0))
    translated_body=db.Column(db.String(10000))
    translated_title=db.Column(db.String(10000))
    subjectivity=db.Column(db.Float(0))
    posted_at = db.Column(db.DateTime) #ToDo: Fix this - currently scraper doesn't scrape posted at.
    is_trafficking = db.Column(db.Boolean(False))
    phone_number = db.Column(db.String(400))

    def __init__(self,text_body='',text_headline='',investigation='',
                 link='',photos='',language='',polarity=0.0,translated_body='',
                 translated_title='',subjectivity=0.0,posted_at=datetime.datetime.now(),
                 is_trafficking=False,phone_number=''):
        self.text_body = text_body
        self.text_headline = text_headline
        self.investigation = investigation
        self.link = link
        self.photos = photos
        self.language = language
        self.polarity = polarity
        self.translated_body = translated_body
        self.translated_title = translated_title
        self.subjectivity = subjectivity
        self.posted_at = posted_at
        self.is_trafficking = is_trafficking
        self.phone_number = phone_number


    def __repr__(self):
        return '<ad %r>' % self.text_headline 

class KeyWords(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(5000))
    
    def __init__(self,keyword):
        self.keyword = keyword

    def __repr__(self):
        return '<keyword %r>' % self.keyword
