from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

from database import db
from datetime import datetime
from enum import Enum

class PlatformEnum(Enum):
    pc = 'pc'
    xbl = 'xbl'
    psn = 'psn'

class RegionEnum(Enum):
    eu = 'eu'
    us = 'us'
    kr = 'kr'
    cn = 'cn'
    gbl = 'global'

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True)
    platform = db.Column(db.Enum(PlatformEnum))
    region = db.Column(db.Enum(RegionEnum))
    stats = db.relationship('Stat', backref='profile',
            cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, tag=None, platform=None, region=None):
        self.tag = tag
        self.platform = platform
        self.region = region

    def __repr__(self):
        return '<Profile %r>' % (self.tag)

class Stat(db.Model):
    __tablename__ = 'stat'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    rank = db.Column(db.Integer)
    stat_date = db.Column(db.Date())

    def __init__(self, profile_id=None, rank=None):
        self.profile_id = profile_id
        self.rank = rank
        self.stat_date = datetime.now()

    def __repr__(self):
        return '<Stat %r>' % (self.profile_id, self.rank, self.stat_date)

ProfileForm = model_form(Profile, base_class=Form, db_session=db.session)
