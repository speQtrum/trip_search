from db import db
from typing import Dict, List

class TripModel(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer,primary_key = True)
    location = db.Column(db.String(15))
    price = db.Column(db.Integer)
    days = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self,location:str,price:float,days:int,user_id:int):
        self.location = location
        self.price = price
        self.days = days
        self.user_id = user_id
    
    def json(self):
        return {
            'location':self.location,
            'price':self.price,
            'days':self.days,
            'user_id':self.user_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_location(cls,location):
        return cls.query.filter_by(location = location).all()

    @classmethod
    def find_my_trips(cls,user_id):
        return cls.query.filter_by(user_id = user_id).all()

    @classmethod
    def all_trips(cls):
        return cls.query.all()