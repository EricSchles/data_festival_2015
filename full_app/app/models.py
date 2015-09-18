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

