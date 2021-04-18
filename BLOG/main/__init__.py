from flask import Blueprint

bp = Blueprint('main', __name__)
print ("main_name:",__name__)
from BLOG.main import routes