### Models for: Comment
### UTELUKKENDE FOR MODELS SOM IKKE HAR RELASJON TIL BRUKER, ELLER RELASJONER TIL OBJEKTER SOM DERETTER ER
### REATERT TIL BRUKER. MODELS KAN VÆRE EN ENKELT FIL, MEN MODELLER OVERHODET IKKE TILKNYTTET BRUKER
### HAVNER HER.

# det er forholdsvis enkelt å konvertere til SQLalchemy,
# men Flask-SQLAlchemy er bedre for å unngå thread error,
# evt kjør SQLAlchemy modeller der du er nøye med session.close etter hver query.
# from BLOG import engine, Base, db_session

# from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
#from sqlalchemy.orm import relationship, backref ## skal ikke behøves

# from BLOG.custom_login import UserMixin, AnonymousUserMixin
from flask import current_app # loxalproxy; skal være factory_måten
from BLOG import db

## ettersom det skapes relationships til Bruker her, importerer vi den:
# from BLOG.Users.models import Bruker ## og det gir circular import issues!
## factory: ingen create_tables
## login_man settes opp som vanlig


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    innhold = db.Column(db.Text())
    forfatter = db.Column(db.String(40), default="anonym")
    dato = db.Column(db.DateTime, default=datetime.now)
    print ("\n db=",db,",in main-Comment Class.")
    def __repr__(self):
        s="ID={} forfatter={} dato={} \n innhold={}" #.format( {self.id}, {self.forfatter}, {self.dato}, {self.innhold})
        return s.format({self.id}, {self.forfatter}, {self.dato}, {self.innhold} ) #{self.id,self.forfatter, self.dato, self.innhold})
    def __add__(self, other):
        if not isinstance(other, Comment):
            print ("Kan kun addere Comments!")
            raise TypeError
        self.innhold=self.innhold+other.innhold
        if len(self.forfatter+other.forfatter)<41:
            self.forfatter=self.forfatter+other.forfatter
        else:
            self.forfatter=self.forfatter
    def __len__(self):
        return len(self.innhold)


# ### LITT OM QUERY:
# # f=Comment.query.all() returnerer en liste som kan loopes med for-loop,
# # det er altså en liste med objekter i. liste: objekt1, objekt2.
# # tilgang til objektene blir som ellers med for x in listen: x.objattributt1 x.objattr2 osv.
# # f.Comment.query.all()
# # for k in f: (ID 1,2,3... ID1=objekt1.innhold osv)
# #   print (k.innhold)
# #   print (k.dato)
# # f=Bruker.query.filter(Bruker.id==2).first() returnerer et objekt; f.brukernavn osv
# # print (f.brukernavn)  <--- går fordi det kun er et objekt med .first()


####################### SE PÅ DETTE ANG SORTERING AV MELDINGER / NYE / DATO: # # # ###
# #     def new_messages(self):                                                     ##
# #         last_read_time = self.last_message_read_time or datetime(1900, 1, 1)    ##
# #         return Message.query.filter_by(recipient=self).filter(                  ##
# #             Message.timestamp > last_read_time).count()                         ##
######################################################################################

# ######## OPPSETTE LOGIN LOADER:
# # @login.user_loader
# # def load_user(id):
# #     return Bruker.query.get(int(id))

# # class AnonymBruker(AnonymousUserMixin):
# #     id=0
# #     fornavn=""
# #     etternavn=""
# #     brukernavn=False
# # login_man.anonymous_user = AnonymBruker

# # followers = db.Table('followers',
# #     db.Column('follower_id', db.Integer, db.ForeignKey('users.id'),primary_key=True, autoincrement=False),
# #     db.Column('followed_id', db.Integer, db.ForeignKey('users.id'),primary_key=True, autoincrement=False)
# # )

# # class Bruker(UserMixin, db.Model):
# #     __tablename__ = "users"

# #     id = db.Column(db.Integer, primary_key=True)
# #     dato = db.Column(db.DateTime, default=datetime.utcnow, index=True)
# #     fornavn = db.Column(db.String(40))
# #     etternavn = db.Column(db.String(40))
# #     brukernavn = db.Column(
# #         db.String(40), index=True, unique=True
# #     )  # unique gir feilmelding hvis forsøkes brutt
# #     rettighet = db.Column(db.String(40), default="bruker")
# #     passord = db.Column(db.String(255))
# #     logindato = db.Column(db.DateTime(), default=datetime.utcnow)
# #     email1 = db.Column(db.String(120), index=True)
# #     password_hash = db.Column(db.String(255))
# #     ### RELATIONSHIPS ####
# #     ### Merk, når en har flere FK som peker mellom samme tables, brukes foreign_keys='Class.var_til_FK'
# #     ### lazy='dynamic' betyr at et nytt query object dannes,
# #     ### dette brukes for å begrense mengden resultat data.
# #     #endre vennskap til venner_med, backref=venner henviser til de som er venner med meg
# #     # vennskap = db.relationship('Bruker', secondary=venner, primaryjoin=(venner.c.bruker_id == id), 
# #     # secondaryjoin=(venner.c.venn_id==id),
# #     # backref=db.backref('venner',lazy='dynamic'),lazy='dynamic')
# #     melding_fra_bruker = db.relationship('Meldinger',foreign_keys='Meldinger.forfatter_id',backref='melding_fra', lazy='dynamic')
# #     melding_til_bruker = db.relationship('Meldinger',foreign_keys='Meldinger.send_til',backref='melding_til', lazy='dynamic')
# #     poster_fra_bruker = db.relationship('UserPost', foreign_keys='UserPost.forfatter_id', backref='poster_fra')
# #     comments_fra_bruker =db.relationship('PostComments', foreign_keys='PostComments.forfatter_id', backref='comments_fra')
# #     annonser_fra_bruker = db.relationship('Annonser', foreign_keys='Annonser.forfatter_id', backref='annonser_fra',lazy='dynamic')

# #     followed = db.relationship(
# #         'Bruker', secondary=followers,
# #         primaryjoin=(followers.c.follower_id == id),
# #         secondaryjoin=(followers.c.followed_id == id),
# #         backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

