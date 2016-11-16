from flask import Blueprint, render_template, redirect, request, url_for
from flask import current_app

from models import *
from database import db
from utils import requires_auth

import requests
import json
from datetime import datetime


rank_api = Blueprint('rank_api', __name__)

def datetime_to_json(d):
    tmp = "Date(%d,%d,%d,%d,%d,%d,0)" %\
            (d.year, d.month-1, d.day, d.hour, d.minute, d.second)
    return tmp 

@rank_api.route('/profile/<id>/ranks/update')
def query_api(id):
    api_url = current_app.config['API_URL']
    profile = Profile.query.filter_by(id=id).first_or_404()
    query_url = '%s/%s/%s/%s/profile' % (api_url, profile.platform.value, profile.region.value, profile.tag)
    resp = requests.get(query_url)

    json_resp = resp.json()['data']
    avatar = json_resp['avatar']
    level = int(json_resp['level'])
    portrait = json_resp['levelFrame']
    star = json_resp['star']
    rank_img = json_resp['competitive']['rank_img']
    rank = int(json_resp['competitive']['rank'])
    rank_obj = Rank(profile.id, rank, avatar, level, portrait, star, rank_img)
    db.session.add(rank_obj)
    db.session.commit()
    return redirect(url_for('rank_api.list_ranks', id=id))

@rank_api.route('/profile/<id>/ranks')
def list_ranks(id):
    profile = Profile.query.filter_by(id=id).first_or_404()
    ranks = profile.ranks.all()
    formatted_ranks = { 'data': map(lambda r: [datetime_to_json(r.rank_date), int(r.rank)], ranks)}
    print json.dumps(formatted_ranks)
    return render_template('rank/list.html', profile=profile, ranks=ranks, formatted_ranks=json.dumps(formatted_ranks))
