""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''
class Pulse(db.Model):
    __tablename__ = 'pulses'  
    _Active = db.Column(db.String(255), primary_key=True)
    _Exercise = db.Column(db.Integer, unique=False, nullable=False)
    
    def __init__(self, Active, Exercise):
        self._Active = Active   
        self._Exercise = Exercise
        
    @property
    def Active(self):
        return self._Active
    
    @Active.setter
    def Active(self, Active):
        self._Active = Active
    
    @property
    def Exercise(self):
        return self._Exercise
   
    @Exercise.setter
    def Exercise(self, Exercise):
        self._Exercise = Exercise
   
    def __str__(self):
        return json.dumps(self.read())
    
    def create(self):
        try:
            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "Active": self.Active,
            "Exercise": self.Exercise
        }

    def update(self, Active="", Exercise=0):
        """only updates values with length"""
        if len(Active) > 0:
            self.Active = Active
        if Exercise >= 0:
            self.Exercise = Exercise
        db.session.commit()
        return self
  
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
"""Database Creation and Testing """

def initPulses():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
       
        pulsestoadd = []
        try:
            with open(r'pulses.json','r') as json_file:
                data = json.load(json_file)
        except Exception as error:
            print("failed")
        for item in data:
            # print(item)
            p_toadd = Pulse(Active=item['Active'], Exercise=item['Exercise'])
            pulsestoadd.append(p_toadd)
        """Builds sample user/note(s) data"""
        for p in pulsestoadd:
            try:
                p.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {p.pulsestoadd}")