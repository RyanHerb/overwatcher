from requests import requests
from json import json
from datetime import datetime

from database import db
from models import *

def query_api(platform, region, profile_id):
    profile = Profile.query.filter_by(id=profile_id).first_or_404()
    query_url = '%s/%s/%s/%s/profile' % (API_URL, platform, region, profile.tag)
    resp = get(query_url)

    json_resp = loads(resp.json())
    stat = Stat(profile.id, int(json_respo['rank']))
    db.session.add(stat)
    db.session.commit()
