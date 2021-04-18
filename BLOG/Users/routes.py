### /Users/routes.py        ### /Users.forms /Users/models /Users/__init__
### MERK: det gir mening å merke disse URL med prefix 'bruker' , husk det eller tilpass det ved tillegg av views
from BLOG.Users import bp  # flask app object/blueprints
from BLOG.custom_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
    login_fresh,
)
from BLOG import db
from BLOG.Users.forms import LoginForm, NyBrukerForm1, PasswordForm
from BLOG.Users.models import AnonymBruker, Bruker
from BLOG.functions.db_func import bruker_query, ny_bruker_db

from flask import flash, request, redirect, render_template, url_for, session
from werkzeug.security import check_password_hash
from datetime import datetime
from random import choice

#### #####                          ------ LOGIN BRUKER VIEW:
@bp.route("/login/", methods=["GET", "POST"])
def login_view():
    user = None
    lyd1 = choice(seq=[True, False, True, False, False])
    if current_user.is_authenticated:
        flash(
            f"Du er allerede logget inn som: {current_user.brukernavn}"
        )  # return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = bruker_query(navn=form.brukernavn.data)
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("users.login_view"))
        # JaNei=login_user(user)
        if login_user(user) == True:
            flash(f"Logget inn med ID: {current_user.id} , {current_user.brukernavn}")
            user.logindato = datetime.utcnow()
            user.passord = "ditt passord er saltet og hashet"
            db.session.add(user)  # login_db)
            db.session.commit()
        # , remember=False)#form.remember_me.data)
        next_page = request.args.get("next")
        ## legges til med validering av korrekt side next_page
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('main.index')
        # return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template(
        "bruker/login.html", title="Sign In", form=form, bruker=user, lyd1=lyd1
    )


@bp.route("/logout/")
@login_required
def logout_view():
    """standard logout view, redirects to index"""
    flash(f"profil: {current_user.brukernavn} er nå logget ut!")
    print(f"\n Logger ut:{current_user.brukernavn}")
    logout_user()
    print(
        f"anonym bruker har ID:{current_user.id} & brukernavn: {current_user.brukernavn}"
    )

    return redirect(url_for("main.index"))


## --------------- OPPRETTE NY BRUKER:
@bp.route("/nybruker/", methods=["GET", "POST"])
def nybruker_view():
    msg = False
    form = NyBrukerForm1()

    if form.validate_on_submit():
        fornavn = form.fornavn.data
        etternavn = form.etternavn.data
        brukernavn2 = form.brukernavn.data
        passord = form.password.data
        email = form.email.data
        valg = form.valg.data
        if valg == "admin" and current_user.is_admin == False:
            msg = "Vokteren svarte at du må vise verdig først!"
        else:
            msg = ny_bruker_db(
                fornavn=fornavn,
                etternavn=etternavn,
                brukernavn=brukernavn2,
                passord=passord,
                email1=email,
                rettighet=valg,
            )

    return render_template(
        "bruker/nybruker.html",
        title="REGISTRERING",
        bruker=current_user,
        msg=msg,
        form=form,
    )


@bp.route("/autorisering/", methods=["GET", "POST"])
@login_required
def autorisering_view():
    """gir brukeren admin rettighet"""
    form = PasswordForm()
    if form.validate_on_submit():
        print("\nBruker ønsker admin rettigheter...")

        if session.get("AdminSuperUser") != None:
            session["AdminSuperUser"] += 1
            print(f"\nAntall forsøk i denne session{session.get('AdminSuperUser')}!")
        else:
            session["AdminSuperUser"] = 1  # gjelder for denne session
        psw = form.password.data
        chkpsw = check_password_hash(
            "pbkdf2:sha256:150000$GZp9Oc5E$a1f116ba0c55c715350d5af171ef9582ca057984ffaf91368e272157ce586665",
            psw,
        )
        if chkpsw == True:
            u = current_user
            # current_user.rettighet="admin"
            u.is_admin=True # via property settes self.rettighet="admin"
            #u.rettighet = "admin"
            print("\n rettigheter gitt")
            ## dersom det nå gjøres en commit vil det vedvare
            db.session.add(u)
            db.session.commit()
        else:
            print ("\nDENIED!")
    return render_template("dev/backdoor.html", form=form)
