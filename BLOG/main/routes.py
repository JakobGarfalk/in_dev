"""benytter app_factory (create_app)
blueprints views"""
### imports fra init:

from flask import (
    request,
    render_template,
    redirect,
    render_template_string,
    flash,
    url_for,
    make_response,
    session,
    escape,
)

# from flask.views import MethodView

from werkzeug.urls import url_parse

# ### import for db kontroll ext:
####### disse hører bare hjemme i /functions/
# from sqlalchemy import text, select,desc,func  ## FJERN?
# from sqlalchemy.orm import query                # FJERNES?


# ERROR HÅNDTERING - HØRER DETTE HJEMME I VIEWS?
# ## error håndtering relegert til BLOG/errors/ modul
# from BLOG.errors.handlers import SomeException
# raise TypeError

from datetime import datetime
from random import choice

### FRA INIT:
from BLOG import db

## men skal vi egentlig bruke db her?
from BLOG.main import bp  # modulens blueprint instans

#### fra main.forms
from BLOG.main.forms import (
    CommentForm1, CommentPost,
    BekreftForm1,
    PostForm1,
    SendMeldingForm1,
    SelectMelding, LocalForm
) ##alle forms for main i main.forms, alle forms for Users.routes i Users.forms

from BLOG.custom_login import current_user, login_required

##############
### MODELS:##### flyttet Bruker modell til BLOG.Users:
from BLOG.main.models import Comment
from BLOG.Users.models import AnonymBruker, Bruker, Dagbok, UserPost, Meldinger, PostComments

#########################################################
# skal erstatte main.db_func , men også etterhvert hete noe annet kanskje?
from BLOG.functions.db_func import (
    bruker_query,
    bruker_query_count,
    les_poster,
    les_comments,
    send_melding,redigere_post
)

####------- KLASSER

# from BLOG.custom_login.utils import login_url, set_login_view

print("Laster main Views...")


@bp.before_request  ### kun utført før requests som inngår i følgende blueprints?
def before_req():
    """før hver request sjekkes bruker auth."""
    if current_user.is_authenticated:
        print("\nMERK OM before req forsvinner når utenfor main:", __name__)
        print(
            f"\n logget inn:{current_user.brukernavn} ID:{current_user.id} admin={current_user.is_admin}"
        )
    else:
        print(
            f"\n anonym={current_user.brukernavn} ID:{current_user.id} admin={current_user.is_admin}"
        )


# @Kontroll.after_request
# def afterfunk(response):
# krever response

# ---Views:---------------------------VIEWS--------------------
@bp.route("/")
@bp.route("/index/")
def index():
    print("INDEX")
    # q=Bruker.query.filter(Bruker.id>0).count()
    brukernavn = current_user.brukernavn
    page = request.args.get("page", 1, type=int)
    comments = les_comments(limit=3, page=request.args.get("page", 1, type=int))
    poster = les_poster(limit=2)
    print("\n current_user.is_admin={}".format(current_user.is_admin))
    next_url = (
        url_for("main.index", page=comments.next_num) if comments.has_next else None
    )
    prev_url = (
        url_for("main.index", page=comments.prev_num) if comments.has_prev else None
    )
    q = bruker_query_count(id=0) ### chk contact
    print(f"\n Query Count type={type(q)}, Count={str(q)}")
    
    return render_template(
        "bruker/index.html",
        title="Rex Vulneratus Est?",
        brukernavn=brukernavn,
        comments1=comments.items,
        poster=poster,
        next_url=next_url,
        prev_url=prev_url,
    )
@bp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    poster = Comment.query.order_by(Comment.dato.desc()).paginate(page, 3, False)
    poster = les_poster(page=page)  # page er en int
    next_url = (
        url_for("main.explore", page=poster.next_num) if poster.has_next else None
    )
    prev_url = (
        url_for("main.explore", page=poster.prev_num) if poster.has_prev else None
    )

    return render_template(
        "bruker/index.html",
        title="Explore",
        poster=False,
        comments1=poster.items,
        next_url=next_url,
        prev_url=prev_url,
    )
#### --------------- BRUKER SIDE VIEWS: #
@bp.route("/bruker/<get_brukernavn>", methods=["GET", "POST"])
@login_required
def brukerside(get_brukernavn):
    form = SendMeldingForm1()
    msg = False
    postkasse=False
    user = current_user if get_brukernavn==current_user.brukernavn else bruker_query(navn=get_brukernavn)

    if user == None: return redirect(url_for("main.index"))  # failsafe
    
    ## followed; en var for db.rel (egentlig et query)
    follow_by = (user.followed.all())#
    follow_me = user.followers.all() #
    ## followers er en backref########

    print(f"\nfollow(ed)_by(_me):{follow_by}/{follow_me}follows")
    print(f"{current_user.brukernavn != get_brukernavn},{current_user.brukernavn},{get_brukernavn}")
    print(f"{current_user.brukernavn == get_brukernavn},{current_user.brukernavn},{get_brukernavn}")
    def _yourpage(user):
        nonlocal postkasse, form
        form = False
        postkasse = Meldinger.query.filter_by(send_til=user.id, lest="ikke lest")
    
    def _visitspage(user):
        nonlocal msg
        
        # dersom request.method=POST skal ikke form.data overskrives
        if request.method=="GET":
            form.send_til.data = user.brukernavn  # form.data må kun fylles i GET requests
        elif form!=False and form.validate_on_submit():
            tittel = form.tittel.data
            innhold = form.innhold.data
            # FORMS.PY SØRGER SELV FOR AT send_til.data er en reell bruker
            # hvis send_til.data matcher en bruker i DB, opprettes: form.objekt_id==bruker.id
            ## dette valideres i forms.py validator:BekfreftBrukernavn
            til_bruker = form.send_til.data #
            til_bruker_id = form.objekt_id  #
            tittel = form.tittel.data
            innhold = form.innhold.data
            # dermed behøves ikke 2 query til db.
            fra_bruker = int(current_user.id)
            m = send_melding(
            tittel=tittel,
            innhold=innhold,
            forfatter_id=fra_bruker,
            send_til_id=til_bruker_id)
            msg = "Melding til {0} er sendt!".format(til_bruker)
    ### SELECTOR FOR YOUR/NOT-YOUR-PAGE: ########
    if user.brukernavn == current_user.brukernavn:
        _yourpage(user=user)
    else:
        _visitspage(user=user)

    return render_template(
        "bruker/bruker_id.html",
        bruker=user,
        form=form,
        postkasse=postkasse,
        msg=msg,
        follow_me=follow_me,
        follow_by=follow_by,
    )
###---------------FOLLOWER FUNK:
@bp.route("/bruker/<get_brukernavn>/follow/")
@login_required  ### det er bare å glemme å sende bruker objekt til funksjonen. Det kan gå an,
def followbruker(
    get_brukernavn,
):  ## men ettersom hvert nye view er frem-tilbake mellom bruker:server
    user = bruker_query(
        navn=get_brukernavn
    )  # spørs det om en engang ønsker å gjøre det.
    # en har i realiteten 2 valg; lagre objektet hos brukeren i en cookie,
    # eller lagre det server-side som user allerede er.
    # at en da må hente frem user obj fra db "unødvendig ofte" er den korrekte måten å håndtere dette på.
    if current_user.is_following(user) == 1:
        current_user.unfollow(user)
        flash(message=f"Sluttet å følge profil: {user.brukernavn}", category="info")
    elif current_user.is_following(user) == 0:
        current_user.follow(user)
        flash(message=f"Følger profil: {user.brukernavn}", category="info")

    db.session.commit()

    return redirect(url_for("main.brukerside", get_brukernavn=get_brukernavn))
###### ------------------------------- LES MELDINGER FUNK:
@bp.route("/bruker/<get_brukernavn>/meldinger/", methods=["GET", "POST"])
@login_required
def bruker_meldinger_view(get_brukernavn):
    # siden vi bruker request.args bør vi ikke trenge **kwargs
    # MERK ANG REQUEST.ARGS;
    # request.args.get('nøkkel') gir None dersom nøkkel mangler
    # å sette request.args kan gjøres via: url_for('view_funk', get_brukernavn=etc, nøkkel=variabelX)
    # når nøkkel & verdi hentes skal = tegn utelates; verdi=request.args.get('nøkkel')
    # i en dynamisk URL som denne vil de dynamiske URL delene som skal til view_funk settes som '/bruker/<til_funk>/'
    # og dermed: def view(til_funk)
    # mens nøkler til request.args ikke skal oppgis i def view(til_funk)
    # request.args skiller første nøkkel fra URL med ? , og deretter &
    # dermed blir flere key:value par => bruker/?k=v&k2=v2&k3=v3

    if not current_user.brukernavn == get_brukernavn:
        return redirect(url_for("users.login_view"))
    
    user = current_user
    msg = False
    form = False
    postkasse = False

    get_kwarg1 = request.args.get("lest_melding")
    # get_arg1=request.args.get('lest',0,type=int)
    print("\nREQ ARGS:", get_kwarg1)

    # merk_lest=url_for('bruker_meldinger_view', get_brukernavn=current_user.brukernavn,lest=1)#meld.id)

    # page = request.args.get('page', 1, type=int)
    # <a href="{{url_for('bruker_meldinger_view', lest=meld.id)}}" class="">Merk som lest</a>
    # poster = Comment.query.order_by(Comment.dato.desc()).paginate(
    #     page, bp.config['POST_PER_PAGE'], False)
    # next_url = url_for('explore', page=poster.next_num) if poster.has_next else None
    # prev_url = url_for('explore', page=poster.prev_num) if poster.has_prev else None
    form = SelectMelding()

    def _lest(get_kwarg1):
        """intern f. henter m:Melding.id==get_kwarg1 & endrer m.lest=utcnow"""
        d = datetime.utcnow()
        lest_dato = d.strftime("%H:%M:%S-%e.%b.%y")
        _id = int(get_kwarg1)
        m = Meldinger.query.filter_by(id=_id).first()
        print("\n _lest melding:", m)
        if m != None:
            m.lest = lest_dato
            db.session.add(m)
            db.session.commit()
        return m

    if get_kwarg1 != None:
        m = _lest(get_kwarg1)  # hent melding dersom

    if form.validate_on_submit():  # and user.brukernavn == current_user.brukernavn:
        # HER TRENGS LOGIKK FOR ALLE, KUN ULESTE, EVT SLETTE?
        valg = form.valg.data
        if valg == "alle":
            postkasse = Meldinger.query.filter_by(send_til=user.id).all()
        if valg == "nye":
            postkasse = Meldinger.query.filter_by(
                send_til=user.id, lest="ikke lest"
            ).all()
        if valg == "slett":
            postkasse = False  # <- OPPSANN!

    return render_template(
        "bruker/bruker_meldinger.html",
        postkasse=postkasse,
        msg=msg,
        bruker=user,
        form=form,
    )

################------------------------# LES & REDIGER DIN SISTE POST #################
@bp.route("/bruker/<get_brukernavn>/siste_post", methods=["GET", "POST"])
@login_required
def bruker_post(get_brukernavn):
    msg = False
    follow_by = False
    follow_me = False
    user = bruker_query(navn=get_brukernavn)
    #user=current_user
    if user==None: return redirect(url_for("main.brukerside"))
    if current_user.brukernavn==user.brukernavn:
        form=PostForm1()
        # form.brukernavn.data = user.brukernavn # settes uanset GET el POST
    else:
        form =None
    post = (
        UserPost.query.filter(UserPost.forfatter_id == user.id)
        .order_by(UserPost.dato.desc())
        .first()
    )

    ## hvis din profil, og du ønsker redigere?
    def make_form(user,post):
        """mat inn user, post. Håndterer GET & POST av form.data & validerer"""
        if post==None: return None
        nonlocal form
        form.brukernavn.data = user.brukernavn
        # if form.validate_on_submit():
        if form.validate_on_submit():
            tittel=form.tittel.data
            slug=form.slug.data
            innhold=form.innhold.data
            forfatter_id=user.id
            id=post.id          # p.oppdatert har en onupdate clause
            msg=redigere_post(id=id,tittel=tittel,slug=slug,forfatter_id=forfatter_id,innhold=innhold)
            flash (msg)

        if request.method=="GET": # dersom GET fyll ut med:
            form.brukernavn.data = user.brukernavn
            form.tittel.data = post.tittel
            form.slug.data = post.slug
            form.innhold.data = post.innhold
        return request.method
    f = make_form(user=user, post=post) if current_user.brukernavn==user.brukernavn else None
    
    ### form er 1. Postform1() 2. PostForm1()+data 3.None
    ### ved POST: 1. ved GET 2. el 3 om ikke din side.
    
    if f=="POST":
            print (f"\nValidering OK, posten opprettet {post.dato} med ID {post.id} er redigert!")
    return render_template(
        "bruker/bruker_post.html",
        bruker=user,
        msg=msg,
        poster=post,
        form=form,
        follow_by=follow_by,
        follow_me=follow_me,
    )


########---------------- REDIGERE BRUKER PROFIL ---------------
@bp.route("/bruker/rediger_profil/", methods=["GET", "POST"])
# @fresh_login_required
def redigere_profil():

    # if form.validate_on_submit():
    #     pass
    # #      current_user.username = form.username.data
    # #     current_user.about_me = form.about_me.data
    # #     db.session.commit()
    # #     flash('Your changes have been saved.')
    # #     return redirect(url_for('edit_profile'))
    # elif request.method == 'GET':
    #     pass
    #     form.username.data = current_user.username
    #     form.about_me.data = current_user.about_me
    return render_template("bruker/dagbok.html", title="Edit Profile")


# @bp.route("/kon/", methods=["GET", "POST"])
# def kontakt_tmp():
#     """Standard `contact` form."""
#     form = ContactForm()
#     if form.validate_on_submit():
#         return redirect(url_for("index"))
#     return render_template("kontakt.html", form=form, template="form-template")


# @bp.route("/contact/", methods=["GET", "POST"])
# def contact():
#     """Standard `contact` form."""
#     form = ContactForm()
#     if form.validate_on_submit():
#         return redirect(url_for("index"))
#     return render_template("contact.jinja2", form=form, template="form-template")


# @bp.route("/kommentarer/", methods=["GET", "POST"])
@bp.route("/kommenter/", methods=["GET", "POST"])
def kommenter():
    # poster = Comment.query.all()
    # comments1=db.session.query(Comment).order_by(desc(Comment.id)).all() #vis siste først
    msg = False

    form = CommentForm1()

    if form.validate_on_submit():  # form er gyldig & method=POST

        innhold = form.innhold.data  # henter data fra FlaskForm
        forfatter = form.forfatter.data
        comment = Comment(innhold=innhold, forfatter=forfatter)
        if current_user.is_anonymous:
            flash("Ettersom du ikke er logget inn, går denne prossesen noe tregere...")

        if innhold == "":
            msg = "Det har skjedd en feil i validering av kommentar skjemaet."
            # LogBug -> opprett en loggerDobbel validering for dette???

        print("ID", comment.id)

        db.session.add(comment)
        db.session.commit()
        msg = "Din kommentar er lagret!"
    # comments1=les_comments(limit=10) # på denne måten ser vi siste postede også
    # unngår post-lag-delay effekt
    page = request.args.get("page", 1, type=int)
    # comments1 = Comment.query.order_by(Comment.dato.desc()).paginate(page, bp.config['POST_PER_PAGE'], False)
    comments1 = les_comments(page=page)
    next_url = (
        url_for("main.kommenter", page=comments1.next_num)
        if comments1.has_next
        else None
    )
    prev_url = (
        url_for("main.kommenter", page=comments1.prev_num)
        if comments1.has_prev
        else None
    )
    paginated_comments = comments1.items
    return render_template(
        "bruker/kommenter.html",
        title="Arkivarium",
        comments1=paginated_comments,
        msg=msg,
        form=form,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/innlegg/", methods=["GET", "POST"])
@bp.route("/poster/", methods=["GET", "POST"])
def innlegg():
    msg = False
    form = PostForm1()
    # poster = UserPost.query.all()
    req_side = request.args.get("page", 1, type=int)
    poster = les_poster(page=req_side)
    # husk at pagination objects må sendes som post.items for å kunne itereres i templat
    # Comment.query.order_by(Comment.dato.desc()).paginate(
    #   page, bp.config['POST_PER_PAGE'], False)
    next_url = (
        url_for("main.innlegg", page=poster.next_num) if poster.has_next else None
    )
    prev_url = (
        url_for("main.innlegg", page=poster.prev_num) if poster.has_prev else None
    )

    if form.validate_on_submit():
        tittel = form.tittel.data
        slug = form.slug.data
        innhold = form.innhold.data
        forfatter = (
            form.brukernavn.data
        )  # forfatter sjekkes mot Brain.BrukerID i form validering
        print("DEBUG:", forfatter, "-form.field. & Session_ID", current_user.id)

        ny = UserPost(
            tittel=tittel, slug=slug, forfatter_id=int(current_user.id), innhold=innhold
        )
        db.session.add(ny)
        db.session.commit()

        msg = "Innlegget er nå lagret i arkivet."

    return render_template(
        "bruker/poster.html",
        title="POSTER",
        poster=poster.items,
        msg=msg,
        form=form,
        brukernavn=current_user.brukernavn,
        next_url=next_url,
        prev_url=prev_url,
    )

@bp.route("/poster/kommentarer/<get_post>", methods=["GET", "POST"])
@login_required
def post_comment(get_post):
    post = UserPost.query.get(int(get_post))
    #innlegg = ["DUMMYDATA U ATTR!","MER DU!DATA U ATTRIB!"]
    if not isinstance(post, UserPost): raise AttributeError

    #PLAN==>trenger en form for postcomments, validering dersom sendt, og at kommentarer hentes her & vises i templat
    innlegg=db.session.query(PostComments).filter_by(post_id=int(get_post)).all()
    form=CommentPost()
    print (innlegg)
    if form.validate_on_submit():
        tittel=form.tittel.data
        innhold=form.innhold.data
        post_id=post.id
        forfatter_id=current_user.id
        cp1= PostComments(tittel=tittel,innhold=innhold,forfatter_id=forfatter_id,post_id=int(get_post))
        db.session.add(cp1)
        db.session.commit()
        flash ("Postet innlegg.")
        return redirect(url_for("main.post_comment", get_post=get_post))

    return render_template("bruker/post_com.html", poster=post, form=form, innlegg=innlegg)


@bp.route("/admin/", methods=["GET", "POST"])
@login_required
def adminfunksjon():
    finnDB = False
    finnPost = False
    msg = False
    if current_user.is_admin:
        msg = "Du er ADMIN"
    else:
        msg = "Du er ingen admin!"
    # if request.method == "GET":

    #     beskjed = "I am the Zentinel. What is your function?"
    #     return render_template("dev/admin.html", title="ADMIN", beskjed=beskjed)

    return render_template(
        "dev/admin.html",
        title="ADMIN",
        poster=Comment.query.all(),
        brukere=Bruker.query.all(),
        oppdrag=finnDB,
        msg=msg,
    )

    if request.method == "POST":
        if (
            "submitfunc" in request.form
        ):  # sjekke navn på submit knapp siden det er flere forms på siden.
            if request.form["admin1"] == "alpha omega":
                Brain.admin = True
                redirect(url_for("main.adminfunksjon"))
        if Brain.admin == False:
            beskjed = "your existence is unclear to us"
            return render_template(
                "dev/admin.html",
                title="ADMIN",
                beskjed=beskjed,
                lyd="spillervoicestayawaymp3",
            )
        if "submit2" in request.form:
            if request.form["Lbrukernavn"] == "":
                msg = "EMPTY SEARCH FIELD!"

            if request.form["Lbrukernavn"] != "":
                reqnavn = request.form["Lbrukernavn"]
                finnDB = Bruker.query.filter(Bruker.brukernavn == reqnavn).first()
                if finnDB != None:
                    # finnPost = UserPost.query.filter(
                    #     UserPost.forfatter_id == finnDB.id
                    # ).all()
                    finnPost = finnDB.poster
                else:
                    msg = "fant ingen slik bruker i DB!"
        return render_template(
            "dev/admin.html",
            title="ADMIN",
            poster=Comment.query.all(),
            brukere=Bruker.query.all(),
            oppdrag=finnDB,
            oppdrag2=finnPost,
            msg=msg,
        )


@bp.route("/dagbok/")
@login_required
def dagbok():
    user=current_user
    en_dagbok=db.session.query(Dagbok).filter(Dagbok.forfatter_id==user.id).first()
    

    return render_template("bruker/dagbok.html", title="DAGBOK", bruker=user)
@bp.route("/only_server/", methods=["GET","POST"])
def local_view1():
    form=LocalForm()
    if form.validate_on_submit():
        tittel=form.tittel.data
        innhold=form.innhold.data
        file="main_local_view1.txt"
        print ("\n-append to file:",file,"\n")
        print (tittel,innhold) # direkte print til fil gir en \n for mye,
        # dette er trolig lagt til av form, og dermed slutter hver linje med \n\n
        # fjerner dette med splitlines og iterer så gjennom listen. 
        #_t=tittel.splitlines()
        _i=innhold.splitlines()
        with open(file=file,mode="a",encoding="UTF-8") as fa:
            print(tittel,file=fa)
            for linje in _i:
                print (linje,file=fa)
            #fa.write(innhold)
            fa.close()
        flash("OK!")

    return render_template("local/welcome.html", form=form)

# class SimpleComment(MethodView):
#     """/kommentarer /arkivarium"""

#     comments = Comment.query.all()  # da blir den konstant resten av session
#     msg = False

#     def __init__(self):
#         self.poster = (
#             SimpleComment.poster
#         )  # selv med oppdatering av klasse verdi blir en liggende en request etter
#         self.comments = Comment.query.all()  # forespørsel til DB for hvert request
#         self.msg = SimpleComment.msg

#         self.form = CommentForm1()

#     def get(self):
#         """ Responds to GET requests """
#         form = self.form
#         return render_template(
#             "bruker/kommenter.html",
#             title="Arkivarium",
#             comments=self.comments,
#             msg=self.msg,
#             brukernavn=self.brukernavn,
#             form=self.form,
#         )

#     def post(self):
#         """ Responds to POST requests """

#         form = self.form
#         kanLagre = False
#         if form.validate_on_submit():
#             comment= Comment(innhold=form.innhold.data, forfatter=form.forfatter.data)
#             kanLagre=True
# #             print(comment)

#         if form.forfatter.data == "" or form.forfatter.data=="anonym":
#             flash("Kommentaren postes anonymt.")
#         if kanLagre == True:
#             db.session.add(comment)
#             db.session.commit()
#             print("ID", comment.id)
#             self.comments = (
#                 Comment.query.all()
#             )  # gir umiddelbar oppdatering, men forlater en siden og kommer tilbake i samme session,
#             # så vil, hvis en bruker klasse var, ikke se de nye postene.

#         # if self.form.validate_on_submit():
#         #     flash('Postet: {}, av:{}'.format(
#         #     self.form.contents, self.form.forfatter))

#         return render_template(
#             "bruker/kommenter.html",
#             title="Arkivarium",
#             comments=self.comments,
#             msg=self.msg,
#             brukernavn=self.brukernavn,
#             form=self.form,
#         )
# bp.add_url_rule("/kommentarer/", view_func=SimpleComment.as_view("kommentarer"))
