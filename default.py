from flask import Blueprint, render_template

from models import Profile, Stat

api = Blueprint('api', __name__)

@api.route('/')
def index():
    profiles = Profile.query.all()
    for profile in profiles:
        profile.last_rank = 0
    return render_template('index.html', profiles = profiles)
