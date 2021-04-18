from BLOG import db

# depenency; kjøres fra flask shell, som bruker create app.
## trenger db engine
from werkzeug.security import generate_password_hash
from BLOG.Users.models import Bruker
from BLOG.functions.db_func import ny_bruker_db

# fornavn1 = [
#     "Adolf",
#     "Ariel",
#     "Camilla",
#     "Coco",
#     "Erna",
#     "Eva",
#     "Gustav",
#     "Iselin",
#     "Knut",
#     "Markus",
#     "Marie",
#     "Oluf",
#     "Siv",
#     "Tor",
# ]
# etternavn1 = [
#     "Ardvark",
#     "Braathen",
#     "Cancer",
#     "Carina",
#     "Collett",
#     "Creosot",
#     "Dinglrot",
#     "Jensen",
#     "Kavli",
#     "Kremer",
#     "Kvitmyr",
#     "Lisdex",
#     "Markali",
#     "Mecklenburg",
#     "Nordhus",
#     "Nyremyr",
#     "Olsen",
#     "Prelltorp",
#     "Solberg",
#     "Trinkelheim",
#     "Werner",
#     "Ødegård",
# ]
# brukernavn1 = [
#     "Alfa",
#     "Ammo",
#     "Astro",
#     "Baby",
#     "Benzin",
#     "Cola",
#     "Crom",
#     "Dekker",
#     "MILF-",
#     "Max",
#     "Mega",
#     "Mekker",
#     "Mora",
#     "Nitro",
#     "Pilsy",
#     "Pyro",
#     "Super",
#     "Toro",
# ]
# brukernavn2 = [
#     "Plugger",
#     "Zuck",
#     "boomer",
#     "boxer",
#     "burner",
#     "cola",
#     "doofus",
#     "fyllik",
#     "gamer",
#     "kaffi",
#     "lick",
#     "sneezer",
#     "snorter",
#     "speed",
#     "splash",
#     "sport",
#     "stormer",
#     "vag'n",
#     "zoomer",
# ]
from random import choice, randint

#from BLOG.functions.automat.automat import Automat
import time


# t = time.process_time()
# #do some stuff
# elapsed_time = time.process_time() - t
class Automat:
    """object contains lists for fornavn,etternavn,brukernavn, & func. gen_users to autogen. Bruker i db"""
    def __init__(self):
        self.fornavn = [
            "Adolf",
            "Ariel",
            "Camilla",
            "Coco",
            "Erna",
            "Eva",
            "Gustav",
            "Iselin",
            "Knut",
            "Markus",
            "Marie",
            "Oluf",
            "Siv",
            "Tor",
        ]
        self.etternavn = [
            "Ardvark",
            "Braathen",
            "Cancer",
            "Carina",
            "Collett",
            "Creosot",
            "Dinglrot",
            "Jensen",
            "Kavli",
            "Kremer",
            "Kvitmyr",
            "Lisdex",
            "Markali",
            "Mecklenburg",
            "Nordhus",
            "Nyremyr",
            "Olsen",
            "Prelltorp",
            "Solberg",
            "Trinkelheim",
            "Werner",
            "Ødegård",
        ]

        self.brukernavn1 = [
            "Alfa",
            "Ammo",
            "Astro",
            "Baby",
            "Benzin",
            "Cola",
            "Crom",
            "Dekker",
            "MILF-",
            "Max",
            "Mega",
            "Mekker",
            "Mora",
            "Nitro",
            "Pilsy",
            "Pyro",
            "Super",
            "Toro",
        ]
        self.brukernavn2 = [
            "Plugger",
            "Zuck",
            "boomer",
            "boxer",
            "burner",
            "cola",
            "doofus",
            "fyllik",
            "gamer",
            "kaffi",
            "lick",
            "sneezer",
            "snorter",
            "speed",
            "splash",
            "sport",
            "stormer",
            "vag'n",
            "zoomer",
        ]

        self.password = generate_password_hash("auto")
        self.rettighet = "bruker"
        self.email1 = "unreal@not.real"
        self.filler = [70,99]
        
    def gen_users(self, ant=1):
        """autogen x(def.1) users"""
        x = 0
        if isinstance(ant, int) == False:
            raise TypeError
        t = time.process_time()
        while x < ant:
            fornavn = choice(self.fornavn)
            etternavn = choice(self.etternavn)
            filler=randint(self.filler[0],self.filler[1]) #for ekstra randomisering av navn
            brukernavn = choice(self.brukernavn1) + choice(self.brukernavn2)+str(filler)
            password = self.password
            email1 = self.email1
            # this will break, brukernavn must be unique;
            #u = Bruker(
            u=ny_bruker_db(
                fornavn=fornavn,
                etternavn=etternavn,
                brukernavn=brukernavn,
                email1=email1,
                passord=password,
            )
            # db.session.add(u)
            # db.session.commit()Timed: 0.859375
            x += 1
            if x>500: break #failsafe
        elapsed_time = time.process_time() - t; print("Timed seconds:",elapsed_time)

#from BLOG.functions.automat.automat import Automat; a=Automat();a.gen_users(10)

## RESULTAT på gen_users(10) - etter dannelse av >100users.
##når SQLALCHEMY_TRACK_MODIFICATIONS=True
#Timed seconds: 0.859375
## når SQLALCHEMY_TRACK_MODIFICATIONS=False:
#Timed seconds: 0.859375
## når SQLALCHEMY_ECHO = False
#Timed seconds: 0.859375