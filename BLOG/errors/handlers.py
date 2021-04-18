from BLOG import db
from BLOG.errors import bp
from flask import render_template #, current_app as app

@bp.app_errorhandler(404)
def not_found_error(error):
    print ("feilkode:404")
    return render_template("error/404_feil.html",title="FEIL:404")

@bp.app_errorhandler(500)
def internal_error(error):
    print ("feilkode:500!")
    db.session.rollback()
    return render_template('error/500_feil.html',title="FEIL:500")
@bp.app_errorhandler(TypeError)
def internal_error(error):
    print (f"\nen {error} har oppstått")

# class SomeException(Exception):
#     def __init__(self, message, errors):
#         # Call Exception.__init__(message)
#         # to use the same Message header as the parent class
#         super().__init__(message)
#         self.errors = errors
#         # Display the errors
#         print('Errors:')
#         print(errors)
        
#


# from flask import current_app as app
# bruker en loxalproxy for error handling.

# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template("error/404_feil.html",title="FEIL:404")
#     # nå blir templates liggende i BLOG/templates/errors
# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('error/500_feil.html',title="FEIL:500")