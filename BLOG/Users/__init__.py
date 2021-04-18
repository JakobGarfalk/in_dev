from flask import Blueprint

bp = Blueprint('users', __name__)
print ("users_name_:",__name__)
from BLOG.Users import routes