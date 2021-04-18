from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField,SubmitField ,StringField, SelectField,PasswordField
from wtforms.validators import InputRequired, EqualTo, Email, ValidationError

from BLOG.custom_login import current_user
from BLOG.functions.db_func import bruker_query
### mine custom validators
### når det blir mange nok av disse legger vi dem i en egen fil under functions/validators.py
## med mulig unntak av de helt spesifikke for Bruker som BekreftBruker;
## etterhvert håper jeg i tillegg til modulæritet, å unngå repeat imports i mange filer,
## men repeat imports vs modulæritet; ytelse vs vedlikehold; dette er Python tross alt.
class ValidateLength(object):
    """tror den er identisk wtforms standard Length validator, men kjekt å ha selv"""
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'må inneholde %i - %i tegn.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)
Lengde=ValidateLength   # 

class BekreftBrukernavn(object):
    """field.data sjekkes mot brukernavn i DB. Hindrer også tomme fields."""
    def __init__(self, message=None):
        if not message:
            message= u'signert brukernavn stemmer ikke med registrert bruker'
        self.message=message
        #self.objekt_id=None
    def __call__(self, form, field):
        signatur=field.data or "" # henter str fra field, eks navn.data
        s = len(signatur) or 0    # tar høyde for evt. missing attr field.data
        if field.name=="brukernavn":
            if signatur.lower()!=current_user.brukernavn.lower():
                raise ValidationError(self.message)
        elif field.name=="send_til":
            if current_user.is_authenticated==False:
                #flash ("Du må være logget inn!")
                self.message="Du er ikke logget inn!"
                raise ValidationError(self.message)

            finn=bruker_query(navn=signatur)
            if finn==None:
                self.message="ugyldig brukernavn"
                raise ValidationError(self.message)
            else:
                form.objekt_id=finn.id # vi gir form en ny attributt
                # dette havner da i form.objekt_id
            
## -
## - FORMS FOR BRUKER LOGIN, OPPRETTING, AUTORISERING, REDIGERING AV PROFIL:

class LoginForm(FlaskForm):
    """brukernavn, password, remember_me, send_knapp"""
    brukernavn = StringField(label="Brukernavn:", validators=[InputRequired(message= "Skriv inn ditt brukernavn!")])
    password = PasswordField(label="Password", validators=[InputRequired(message="Fyll inn korrekt passord!")])
    remember_me = BooleanField('Remember Me', default=False)
    send_knapp=SubmitField(label="LOGIN")

class NyBrukerForm1(FlaskForm):
    """fornavn, etternavn,brukernavn,password,email,valg """
    fornavn = StringField(label="Fornavn:", validators=[Lengde(min=1, max=40, message="%(min)d - %(max)d tegn!")])
    etternavn = StringField(label="Etternavn:", validators=[Lengde(min=1, max=40, message="%(min)d - %(max)d tegn!")])
    brukernavn = StringField(label="Brukernavn:", validators=[Lengde(3, 40, "brukernavn skal inneholde %(min)d - %(max)d tegn!")])
    password = StringField(label="Passord:", validators=[Lengde(min=4, max=80, message="%(min)d - %(max)d tegn!")])
    confirm_password = StringField(label='Gjenta passord',validators=[EqualTo(fieldname="password", message='Passord må matche.')])
    email = StringField(label='Email', validators=[Email(message='Not a valid email address.'),Lengde(min=4, max=120, message="%(min)d - %(max)d tegn!")])
    valg = SelectField(label='Jeg er:',validators=
        [InputRequired(message="Gjør et valg!")],
        choices=[
            ('bruker', 'en vanlig bruker'),
            ('gjestebruker', 'en gjest på besøk'),
            ('admin', 'en Administrator (må godkjennes av Vokteren)'),
            ('moderator', 'en Moderator'),
            ('hacker', 'et uønsket element'),
            ('politisk korrekt', 'ikke enig i denne kategorisering av min person')
        ]
    )
    send_knapp=SubmitField(label="REGISTRER NY BRUKER")

class PasswordForm(FlaskForm):
    password=PasswordField(label="Hvorfor skal du autoriseres?", validators=[InputRequired(message="FEIL!")])