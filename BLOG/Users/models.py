from sqlalchemy.orm import backref
from BLOG import db, login_man
from BLOG.custom_login import UserMixin, AnonymousUserMixin

# from BLOG.main.models import UserPost
## alle modellene må kanskje ligge sammen for å unngå circular imports,
## men forsøker først med kun de der enten Bruker eller modell spesifikt nevner hverandres klasser.

from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

""" users består av modellene: AnonymBruker, Bruker
utfører også her logikk i forhold til login.manager.user_loader
## vurderer å etterhvert lage en ny bruker klasse som skal hete 'User',"""


@login_man.user_loader
def load_user(id):
    # .get(int(id)) id primary keys i SQL DB, er INTEGER, mens login_man bruker STR.
    # derfor må en konvertere TIL INT når en henter fra load_user
    return Bruker.query.get(int(id))


class AnonymBruker(AnonymousUserMixin):
    id = 0
    fornavn = ""
    etternavn = ""
    brukernavn = False


login_man.anonymous_user = AnonymBruker

followers = db.Table(
    "followers",
    db.Column(
        "follower_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        autoincrement=False,
    ),
    db.Column(
        "followed_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
        autoincrement=False,
    ),
)


class Bruker(UserMixin, db.Model):
    __tablename__ = "users"
    print ("\n db=",db,",in Users-Bruker Class&name=",__name__)
    
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fornavn = db.Column(db.String(40))
    etternavn = db.Column(db.String(40))
    brukernavn = db.Column(
        db.String(40), index=True, unique=True
    )  # unique gir feilmelding hvis forsøkes brutt
    rettighet = db.Column(db.String(40), default="bruker")
    passord = db.Column(db.String(255))
    logindato = db.Column(db.DateTime(), default=datetime.utcnow)
    email1 = db.Column(db.String(120), default="allowdoubles@dev.tmp")
    password_hash = db.Column(db.String(255))
    ### RELATIONSHIPS ####
    ### Merk, når en har flere FK som peker mellom samme tables, brukes foreign_keys='Class.var_til_FK'
    ### lazy='dynamic' betyr at et nytt query object dannes,
    ### dette brukes for å begrense mengden resultat data.
    # endre vennskap til venner_med, backref=venner henviser til de som er venner med meg
    # vennskap = db.relationship('Bruker', secondary=venner, primaryjoin=(venner.c.bruker_id == id),
    # secondaryjoin=(venner.c.venn_id==id),
    # backref=db.backref('venner',lazy='dynamic'),lazy='dynamic')
    melding_fra_bruker = db.relationship(
        "Meldinger",
        foreign_keys="Meldinger.forfatter_id",
        backref="melding_fra",
        lazy="dynamic",
    )
    melding_til_bruker = db.relationship(
        "Meldinger",
        foreign_keys="Meldinger.send_til",
        backref="melding_til",
        lazy="dynamic",
    )
    poster_fra_bruker = db.relationship(
        "UserPost", foreign_keys="UserPost.forfatter_id", backref="poster_fra"
    )
    comments_fra_bruker = db.relationship(
        "PostComments", foreign_keys="PostComments.forfatter_id", backref="comments_fra"
    )
    annonser_fra_bruker = db.relationship(
        "Annonser",
        foreign_keys="Annonser.forfatter_id",
        backref="annonser_fra",
        lazy="dynamic",
    )
    followed = db.relationship(
        "Bruker",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    min_dagbok=db.relationship("Dagbok", foreign_keys="Dagbok.forfatter_id", backref="dagbok")

    def __repr__(self):
        return f"<ID: {self.id}, brukernavn={self.brukernavn},logindato= {self.logindato}>"  # , venner= {self.vennskap}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        # return

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(
        self, user
    ):  # UserPost.query.join(followers, (followers.c.followed_id == UserPost.user_id))
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def only_followed_posts(self):
        return (
            UserPost.query.join(
                followers, (followers.c.followed_id == UserPost.forfatter_id)
            )
            .filter(followers.c.follower_id == self.id)
            .order_by(UserPost.dato.desc())
        )

    def followed_posts(self):
        followed = UserPost.query.join(
            followers, (followers.c.followed_id == UserPost.forfatter_id)
        ).filter(followers.c.follower_id == self.id)
        own = UserPost.query.filter_by(forfatter_id=self.id)
        return followed.union(own).order_by(UserPost.dato.desc())

    def obj_til_dict(self):
        """hent query objekt, få dikt i var d = Bruker.objtildikt(queryobj)
        ex. finnDB1 = Bruker.query.filter(Bruker.brukernavn == "Jdg").first()
        d = Bruker.objtildikt(finnDB1)"""
        dict_var = {
            "id": self.id,
            "dato": self.dato,
            "fornavn": self.fornavn,
            "etternavn": self.etternavn,
            "brukernavn": self.brukernavn,
            "email1": self.email1,
            "passord": self.passord,
            "password_hash": self.password_hash,
            "logindato": self.logindato,
        }
        return dict_var


class UserPost(db.Model):
    """{% for post in poster %}
    <h2>{{ post.tittel }}</h2>
    <small>forfatter: {{ post.poster_fra.fornavn }} {{ post.poster_fra.etternavn }} </small>"""

    __tablename__ = "poster"
    id = db.Column(db.Integer(), primary_key=True)
    tittel = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.Text(), nullable=False)
    innhold = db.Column(db.Text(), nullable=False)
    dato = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    oppdatert = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    ### FOREIGN KEYS:
    forfatter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #### RELATIONSHIPS: ####
    # forfatter=db.relationship("Bruker", backref="poster") #flyttet til Bruker
    comment_rel = db.relationship(
        "PostComments",
        foreign_keys="PostComments.post_id",
        backref="comments_on_post",
        lazy="dynamic",
    )
    
    def __repr__(self):
        return f"ID: {self.id} {self.tittel} {self.forfatter_id}"
    @property
    def fortell(self):
        #self.egenskap=self.innhold
        return self.fortelling
    @fortell.setter
    def fortell(self, verdi=1):
        self.fortelling=self.innhold if verdi==1 else self.tittel+"\n"+self.slug+"\n"+self.innhold
        return self.fortelling

    # siste=UserPost.query.filter(UserPost.forfatter_id==current_user.id).order_by(UserPost.dato.desc())


class PostComments(db.Model):
    """post_id=FK poster.id"""

    __tablename__ = "postcomments"
    id = db.Column(db.Integer(), primary_key=True)
    tittel = db.Column(db.String(255), nullable=False)
    innhold = db.Column(db.Text(), nullable=False)
    ### FOREIGN KEYS:
    post_id = db.Column(
        db.Integer, db.ForeignKey("poster.id")
    )  # UserPost backref=comments
    forfatter_id = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )  # Bruker backref=comments


class Annonser(db.Model):
    __tablename__ = "annonser"
    id = db.Column(db.Integer, primary_key=True)
    tittel = db.Column(db.String(255), nullable=False)
    innhold = db.Column(db.String(4096))
    kategori = db.Column(db.String(255), nullable=False)
    forfatter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # annonser = db.relationship('Bruker', foreign_keys='forfatter.id', backref='mine_annonser',lazy='dynamic')


class Meldinger(db.Model):
    __tablename__ = "meldinger"
    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.DateTime, default=datetime.now, index=True)
    tittel = db.Column(db.String(255))
    innhold = db.Column(db.String(1024))
    forfatter_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    send_til = db.Column(db.Integer, db.ForeignKey("users.id"))
    lest = db.Column(db.String(25), default="ikke lest")

    @property
    def status(self):
        #self.status = "new" if self.lest=="ikke lest" else "old"
        return self.status
    @status.setter
    def status(self, verdi):
        if verdi == "new": 
            self.lest="ikke lest" #if verdi=="new" else datetime.now
            self.status="new"
        else:
            print ("\nkun new er slå langt implementert")
            raise TypeError
        



class Dagbok(db.Model):
    __tablename__ = "dagbok"

    id = db.Column(db.Integer, primary_key=True)
    dato = db.Column(db.DateTime, default=datetime.now, index=True)
    oppdatert = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    ### RELATIONSHIPS: Bruker.min_dagbok
    forfatter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ant_sider = db.Column(db. Integer, db.ForeignKey('dagbok_side.id'))
### en dagbok pr bruker -dagbok.forfatter_id
### flere sider pr dagbok -> dagbok.ant_sider FK - dagbokSide.id
###                                                dagbokSide.innhold
#     side = db.Column(db.Integer)
class DagbokSide(db.Model):
    __tablename="dagbok_side"
    id = db.Column(db.Integer, primary_key=True)
    i_dagbok=db.relationship("Dagbok", foreign_keys="Dagbok.ant_sider",backref="side")
    innhold = db.Column(db.Text())