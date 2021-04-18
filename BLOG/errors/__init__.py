from flask import Blueprint

bp = Blueprint(name='errors',import_name=__name__)

## Error handling uten blueprint bør da også virke:


from BLOG.errors import handlers