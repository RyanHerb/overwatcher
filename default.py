from flask import Blueprint, render_template

from models import Report, Server, Field, Format
from utils import get_mapped_dict, get_processor
from comparator import Status, calculate_status

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html', servers=server_list, formats=formats)
