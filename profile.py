from flask import Blueprint, render_template, redirect, request, url_for

from models import *
from database import db
from utils import requires_auth

profile_api = Blueprint('profile_api', __name__)

@profile_api.route('/profile/add', methods=['GET', 'POST'])
def add():
    if (request.method == 'GET'):
        return serve_form()
    return process_form()

@profile_api.route('/profile/<id>/edit', methods=['GET', 'POST'])
@requires_auth
def edit(id):
    profile = Profile.query.filter_by(id=id).first_or_404()
    if request.method == 'GET':
        return serve_form(profile)
    return process_form(profile)

@profile_api.route('/profile/<id>/confirm')
@requires_auth
def confirm(id):
    my_profile = Profile.query.filter_by(id=id).first_or_404()
    confirm_url = url_for('profile_api.delete', id=id)
    cancel_url = url_for('api.index')
    return render_template('confirm.html', confirm_url=confirm_url, cancel_url=cancel_url)

@profile_api.route('/profile/<id>/delete')
@requires_auth
def delete(id):
    p = Profile.query.filter_by(id=id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('api.index'))

def serve_form(profile=None):
    form = ProfileForm(obj=profile)
    action = url_for('profile_api.add') if profile is None else url_for('profile_api.edit', id=profile.id)
    return render_template('profile/form.html', form=form, action=action)

def update_profile(tag, platform, region, profile=None):
    if profile is None:
        return Profile(tag, platform, region)
    profile.tag = tag
    profile.platform = platform
    profile.region = region
    return profile

def process_form(profile=None):
    tag = request.form['tag']
    platform = request.form['platform']
    region = request.form['region']
    
    my_profile = update_profile(tag, platform, region)
    form = ProfileForm()
    try:
        if profile is None:
            action = url_for('profile_api.add')
            db.session.add(my_profile)
        else:
            action = url_for('profile_api.edit', id=profile.id)
        db.session.commit()
        return redirect(url_for('api.index'))
    except:
        db.session.rollback()
    form.tag.errors = ['That tag already exists']
    action = '/profile/add'
    return render_template('profile/form.html', form=form, action=action)
