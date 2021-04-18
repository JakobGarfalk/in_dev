"""
/functions/
bruker_query returnerer 1 bruker,
bruker_query_count : teller brukere fra id=0 eller oppgitt id.
func: bruker_fra_db, ny_bruker_db, (erstatter loginbruker.py)
les_comments, les_poster, send_melding
"""
from time import sleep
from flask.globals import current_app

from BLOG import db
# dersom models importeres her kan en risikere circular import crash

# from BLOG.main.models import Comment, UserPost, Meldinger
from BLOG.main.models import Comment
from BLOG.Users.models import Bruker, UserPost, Meldinger
from sqlalchemy import text, func, desc
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt

# from multiprocessing import Process
# from datetime import datetime

""" 
## LITT OM QUERY OPS:
q=Bruker.query.filter(Bruker.id>0).count()
#--> gir en INT, i dette tilfellet antall brukere.
.filter(func.lower(Bruker.brukernavn))==    lowercase, husk import text, ->func, desc fra SQLalchemy
.order_by(UserPost.dato.desc()).paginate(side, poster pr side, False)
#--> gir pagination objekt, display som dikt.
#### .paginate(1,4,False) betyr; vi er på side 1, 4 poster pr side, errormsg=False - hvis True vil en tom liste gi 404 feil.
comments=db.session.query(Comment).order_by(desc(Comment.id)).limit(3) #gir siste 3 basert på id

### QUERY MED JOIN:
# Meldinger.forfatter_id=FK 'users.id' 
u1=Bruker.query.join(Meldinger, (Meldinger.forfatter_id==Bruker.id)).filter(Bruker.id==11).first()
"""
# class Crapper(object):
#     def __init__(self, app=None, db=None):
#         self.app=app
#         self.purpose=[1,2,3,4,5,6,7,8]
#         if not app==None:
#             self.init_crap(app, db)

#     def init_app(self, app, db):
#         app.crapper=self
#         self.db=db
from multiprocessing import Process
from datetime import datetime

def a_process(tid=float(1)):
    start_tid=datetime.utcnow()
    print (f"Sleep i {tid} sec.")
    sleep(tid)
    print ("awoke now!")
    end_tid=datetime.utcnow()
    intervall=end_tid-start_tid
    print (f"intervall={intervall}")
    return 0
def call_a_process():
    p=Process(target=a_process, args=[3.0])
    p.start()
    b=ny_bruker_db(fornavn="Eva",etternavn="Sch",brukernavn="EvaSch",passord='auto')
    p.join(timeout=10)
    q=input ("query:")
    u1=db.session.query(Bruker).filter_by(fornavn=q).first()
    print (u1)
# from BLOG.functions.db_func import a_process, call_a_process; db.create_all(); t=call_a_process()


def bruker_query(navn="", id=0):
    
    """hvis id oppgis returneres Bruker.query(--).first() objekt, hvis bare navn oppgis returneres Bruker.query(brukernavn).first()"""
    # navn = ""
    # id=0
    ### id har presedens over navn:
    if int(id) > 0:
        b = db.session.query(Bruker).filter(Bruker.id == id).first()
        # if navn=="" and b!=None: return b #ønsker vi 2 query's dersom None? Nei.
    b = (
        db.session.query(Bruker)
        .filter(func.lower(Bruker.brukernavn) == func.lower(navn))
        .first()
    )
    return b


def bruker_query_count(navn="", id=0):
    """telle hvor mange brukere had id>0 eller oppgitt id"""
    if navn == "":  # uten oppgitt navn returneres ant.brukere med id>oppgitt id, def=0
        b = Bruker.query.filter(Bruker.id > id).count()
        return b
    print("hva trenger vi telle på andre måter enn id?")


def bruker_fra_db(reqnavn=None, reqID=None):
    """Oppgi reqnavn, ELLER reqID & få returnert Bruker.query.object.first()"""

    if not reqnavn == False and not reqnavn == None:
        finnDB1 = (
            db.session.query(Bruker)
            .filter(func.lower(Bruker.brukernavn) == func.lower(reqnavn))
            .first()
        )
    if not reqID == None and reqnavn == None:
        _reqID = int(reqID)
        # finnDB1 = (db.session.query(Bruker).filter(Bruker.id==_reqID).first())
        db.session.query(Bruker).get(_reqID)
    return finnDB1


def ny_bruker_db(
    fornavn="Zoe",
    etternavn="Quinn",
    brukernavn="ZoeQu",
    email1="ZoeQ@local.ho",
    rettighet="bruker",
    passord="python",
):
    """oppretter ny bruker, return msg string"""
    password_hash = generate_password_hash(passord, salt_length=200)

    prevent_double = bruker_fra_db(reqnavn=brukernavn)
    if prevent_double != None:
        msg = "Brukernavn er allerede i bruk!"
        return msg
    else:
        ny = Bruker(
            fornavn=fornavn,
            etternavn=etternavn,
            brukernavn=brukernavn,
            email1=email1,
            rettighet=rettighet,
            passord="passord saltes og hashes før lagring i databasen",
            password_hash=password_hash,
        )
        db.session.add(ny)
        db.session.commit()
        beskjedSTR = "bruker: " + ny.brukernavn + " legges til med ID:" + str(ny.id)
        # flash(beskjedSTR)
        msg = beskjedSTR
    return msg


def les_comments(limit=3, page=""):
    """default returns 3 comments
    PAGINATION objects må sendes som som c.items dersom de skal itereres"""
    ### DET ER ALDRI EN GOD LØSNING Å MÅTTE IMPORTERE I HVER FUNK, TENK PÅ RESTRUKTURERING!
    from BLOG.main.models import Comment
    config = current_app.config

    COMMENTS_PER_PAGE = config.get("COMMENTS_PER_PAGE", 1)
    POST_PER_PAGE = config.get("POST_PER_PAGE", 1)
    # COMMENTS_PER_PAGE=Kontroll.config['COMMENTS_PER_PAGE'] or 1
    if page == "":
        c = db.session.query(Comment).order_by(desc(Comment.id)).limit(limit)
    else:
        c = Comment.query.order_by(Comment.dato.desc()).paginate(
            page, COMMENTS_PER_PAGE, False
        )
    return c


def les_poster(limit=0, page=""):
    """å kalle denne funksjonen uten argument gir error
    args: limit=int, page=int eller "alle"
    HUSK AT PAGINATION OBJECTS OPPFØRER SEG LITT ANNERLEDES;
    dvs. istedenfor å sende poster, må en sende poster.items til templat for iterering.
    default returns 1 (siste) post"""
    
    config = current_app.config
    COMMENTS_PER_PAGE = config.get("COMMENTS_PER_PAGE", 1)  # get('X',defaultverdi)
    POST_PER_PAGE = config.get("POST_PER_PAGE", 1)  # hvis ikke key finnes settes 1
    # POST_PER_PAGE=Kontroll.config['POST_PER_PAGE'] or 1

    if isinstance(page, int):
        # page er i dette tilfellet en int
        p1 = (
            db.session.query(UserPost)
            .order_by(UserPost.dato.desc())
            .paginate(page, POST_PER_PAGE, False)
        )
        print("\n utført les_poster klausul not page==\n return .paginate: ", p1)
        # p1 = db.session.query(UserPost).order_by(desc(UserPost.id)).xxx()
    elif page == "alle":
        p1 = db.session.query(UserPost).order_by(desc(UserPost.id)).all()
        print("\n utført les_poster klausul not page==alle\n return .all: ", p1)
    elif limit > 0:
        p1 = db.session.query(UserPost).order_by(desc(UserPost.id)).limit(limit)
        print("\n utført les_poster klausul limit>0\n return .limit: ", p1)
    return p1


def send_melding(tittel, innhold, forfatter_id, send_til_id, lest="ikke lest"):
    """tittel, innhold, fra_bruker(id), til_bruker(id)
    returns str "id={2}fra={0},til={1}"""
    
    m1 = Meldinger(
        tittel=tittel,
        innhold=innhold,
        forfatter_id=forfatter_id,
        send_til=send_til_id,
        lest=lest,
    )
    ## i models.py har lest default verdi som "ikke lest", så den behøver ikke oppgis.
    ## men ettersom send_melding kan gjenbrukes i les_melding og sett lest="sett"
    db.session.add(m1)
    db.session.commit()
    if hasattr(m1,"id")==False:
        x=input ("WHAT?")
    return "id={2}fra={0},til={1}".format(forfatter_id, send_til_id,m1.id)

def redigere_post(id,tittel, slug, forfatter_id, innhold="Det var en gang"):
    edit_p=UserPost.query.get(id)
    edit_p.tittel=tittel
    edit_p.slug=slug
    edit_p.innhold=innhold
    # (tittel = tittel,slug=slug, forfatter_id=forfatter_id, innhold=innhold)
    db.session.add(edit_p)
    db.session.commit()
    msg="redigert id:{}poster:{}dato:{}oppdatert:{}\ntittel:{}".format({edit_p.id},{edit_p.forfatter_id},{edit_p.dato},{edit_p.oppdatert},{edit_p.tittel})
    return msg

def ny_post_db(tittel, slug, forfatter_id, innhold="Det var en gang"):
    
    pny1 = UserPost(
        tittel=tittel, slug=slug, forfatter_id=forfatter_id, innhold=innhold
    )
    db.session.add(pny1)
    db.session.commit()
