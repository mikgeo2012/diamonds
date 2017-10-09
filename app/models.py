from app import db
import json
import web_scraper
import os
# from database import DataBase as DB


# diamonds_users_table = db.Table('diamonds_users_table',
#                                       db.Column('id', db.Integer, primary_key=True),
#                                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#                                       db.Column('diamond_id', db.Integer, db.ForeignKey('diamond.id'))
# )

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # diamonds = db.relationship('diamond', secondary=diamonds_users_table, backref='user')

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Diamond(db.Model):
    __tablename__ = 'diamond'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    carat = db.Column(db.Float)
    color = db.Column(db.String(1))
    clarity = db.Column(db.String(4))
    url =  db.Column(db.String(2048), index=True)
    gia_num = db.Column(db.Integer)
    depth = db.Column(db.Float)
    table = db.Column(db.Float)
    crown = db.Column(db.Float)
    pavilion = db.Column(db.Float)
    culet = db.Column(db.Integer)
    diameter = db.Column(db.Float)
    cut_score = db.Column(db.Float)
    hca_score = db.Column(db.Float)
    dim = db.Column(db.String(15))
    cut = db.Column(db.String(15))
    shape = db.Column(db.String(15))
    dia_carat = db.Column(db.Float)


    def __init__(self, **kwargs):
        super(Diamond, self).__init__(**kwargs)



    def __repr__(self):
        return '<Diamond {0}><url {1}>'.format(self.id, self.url)




