"""form skjemaer til bruker input definert her: /n
CommentForm1;innhold,forfatter
LoginForm; username, password
NyBrukerForm1, BekreftForm1
på både PostForm1 & SendMeldingForm1 er det en custom validator; BekreftBrukernavn
BekfreftBrukernavn krever, hvis field.brukernavn; at form.brukernavn.data==current_user.brukernavn
hvis field.send_til; at form.send_til.data == user hentet fra DB, dvs NOT==None
& skaper en attributt som blir hetende form.objekt_id ; == bruker.id (dermed slipper en spørre DB etter bruker.ID)
"""
from flask.app import Flask
from flask.globals import current_app
from wtforms.fields.simple import HiddenField
from BLOG.custom_login import current_user
from flask_wtf import FlaskForm,RecaptchaField, recaptcha
from wtforms import Form, StringField, PasswordField, TextAreaField, SubmitField,SelectField,DateField,BooleanField
from wtforms.validators import (
    InputRequired,
    ValidationError,
    DataRequired,
    EqualTo,
    Email,Regexp
)
from flask import flash
##import for db:
#from BLOG.models import Bruker
# from BLOG.main.models import Bruker
from BLOG.Users.models import Bruker
from BLOG.functions.db_func import bruker_query
### for å danne egne enkle validerinsfelt i form
# from random import choice
# tilfeldig=['Q','W','E','R','T','Y']
# velg_en=choice(tilfeldig)
# config=current_app.config
# RECAPTCHA_PUBLIC_KEY=config.get(RECAPTCHA_PUBLIC_KEY)
# RECAPTCHA_PRIVATE_KEY=config.get(RECAPTCHA_PRIVATE_KEY)
#RECAPTCHA_API_SERVER 	optional Specify your Recaptcha API server.
#RECAPTCHA_PARAMETERS 	optional A dict of JavaScript (api.js) parameters.
#RECAPTCHA_DATA_ATTRS

class CustomLength(object):
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
            #finn = Bruker.query(Bruker).filter(func.lower(Bruker.brukernavn)==func.lower(signatur).first()

        #finn = Bruker.query(Bruker).filter(Bruker.brukernavn.ilike(signatur)).first()
        #print ("/n DEBUG: custom_validator chk DB=",finn,"& field_data=",field.data,"vs sign.",signatur)
        
#et re = /[^ \w]/g 
Lengde = CustomLength
#var re = /^[ A-Za-z0-9_@./#&+-]*$/
# <[^<>]+>
ugyldig = Regexp(regex="\\w+", message="Ugyldige tegn!")
# forbidden=">]</[\@&{"
#     match = re.search(forbidden, orginal)
#ugyldig=Regexp(regex="></\@&{",message="Ugyldige tegn!")


class CommentForm1(FlaskForm):
    """(FlaskForm) field_name: innhold, forfatter, send_knapp. ex: reqdata=form.innhold.data"""
    #innhold = TextAreaField(label="Skriv en kommentar:",validators=[Length(min=10, max=4096, message="Må inneholde %(min)d - %(max)d tegn!")],render_kw={"placeholder": "Jeg husker det var...","rows":"5","col":"300","style":"width:600px; heigth:300px"})
    innhold = TextAreaField(label="Skriv en kommentar:",validators=[Lengde(min=10, max=4096)],render_kw={"placeholder": "Jeg husker det var...","rows":"5","col":"300","style":"width:600px; heigth:300px"})
    forfatter = StringField(label="Hilsen:", default="anonym")
    send_knapp = SubmitField(label="SEND POST")
class CommentPost(FlaskForm):
    """debatt innlegg på UserPost"""
    tittel=StringField(label="Emne:", validators=[Lengde(min=3, max=255)],render_kw={"style":"width:900px; heigth:100px"})
    innhold=TextAreaField(label="Innhold:", validators=[Lengde(min=5, max=4096)],render_kw={"rows":3,"col":300,"style":"width:900px; heigth:200px"})
    #post_id
    #forfatter_id
    send_knapp=send_knapp=SubmitField(label="POST KOMMENTAR")

class SelectMelding(FlaskForm):
    """valg:nye,alle,slett"""
    valg=SelectField(label="VIS MELDINGER",validators=[InputRequired(message="Velg fra menyen")],
    choices=[('nye',"les nye meldinger"),
    ('alle','se alle meldinger'),
    ('slett',"slett leste meldinger"),
    ])
    send_knapp=SubmitField(label="UTFØR")

class PostForm1(FlaskForm):
    """tittel, slug, innhold, brukernavn(sjekkes mot Brain.bruker), send_knapp"""
    tittel = StringField(label="Tittel:", validators=[Lengde(min=5, max=255)],render_kw={"style":"width:900px; heigth:100px"})
    slug   = TextAreaField(label="Tema/slug:", validators=[Lengde(min=5, max=500)],render_kw={"rows":3,"col":300,"style":"width:900px; heigth:200px"})
    innhold= TextAreaField(label="Innhold:", validators=[Lengde(min=5, max=4096)],render_kw={"placeholder": "Det var en gang...","rows":"5","col":"300","style":"width:900px; heigth:500px"})
    brukernavn=StringField(label="Bekreft ditt brukernavn:", validators=[BekreftBrukernavn()])
    #recaptcha=RecaptchaField() #bruker Google
    send_knapp=SubmitField(label="POST")

class SendMeldingForm1(FlaskForm):
    tittel = StringField(label="Emne:", validators=[ugyldig,Lengde(min=5, max=255)])
    innhold = TextAreaField(label="Melding:", validators=[ugyldig,Lengde(min=5, max=1024)],render_kw={"placeholder": "Hei!","rows":5,"col":300,"style":"width:600px; heigth:300px"})
    send_til= StringField(label="Til brukernavn:", default="", validators=[BekreftBrukernavn()])
    send_knapp=SubmitField(label="SEND")

# class EditProfilForm1(FlaskForm):
#     pass

class BekreftForm1(FlaskForm):
    """default label=SEND"""
    send_knapp=SubmitField(label="SEND")
class LocalForm(FlaskForm):
    tittel = StringField(label="Dag/emne:", validators=[Lengde(min=2, max=255)],render_kw={"style":"width:900px; heigth:100px"})
    innhold= TextAreaField(label="Innhold:", validators=[Lengde(min=5, max=4096)],render_kw={"placeholder": "Notering","rows":"5","col":"300","style":"width:900px; heigth:500px"})
    send_knapp=SubmitField(label="SEND")
class ContactForm(FlaskForm):
    """Contact form."""

    name = StringField("Name", [DataRequired()])
    email = StringField(
        "Email", [Email(message=("Not a valid email address.")), DataRequired()]
    )
    body = TextAreaField(
        "Message",
        [DataRequired(), Lengde(min=4, message=("Your message is too short."))]
    )
    #recaptcha = RecaptchaField() #Recap. baserer seg på google, må definere RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
    submit = SubmitField("Submit")
#  EKS PÅ EDITcustom FORM, men en kan lettere bruke form(obj=bruker) for å sende med et objekt
# class EditForm(RegisterForm):
#     def __init__(self, member, *args, **kwargs):
#         super(EditForm, self).__init__(*args, **kwargs)
#         self.name.data = member.name
#         self.phone.date = member.phone