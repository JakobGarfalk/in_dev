
from BLOG import create_app, db
from BLOG.main.models import Comment
from BLOG.Users.models import Bruker,UserPost,Meldinger, PostComments
from datetime import datetime
app = create_app()



@app.shell_context_processor
def make_shell_context():
    print ("\n(db ,UserPost kortes ned til Post, Bruker, PostComments til PC, Meldinger, Comment)")
    print ("\n(### SHELL CONTEXT TERMINAL - create_app() fra BLOG.__init__ - db engine=original ### ")
    print ("\n evt. copy: \nfrom BLOG.Users.models import Bruker,UserPost,Meldinger, PostComments\nBLOG.main.models import Comment")
    return {'db': db, 'Post': UserPost, 'Bruker': Bruker, 'Meldinger': Meldinger,"PC":PostComments,"Comment":Comment}


# class Book():
#     def __init__(self,user):
#         self.entries=[]
#         self.bruker=user
#     def add_entry(self, nyrutine):
#         self.entries.append(nyrutine)
#     def save(self):
#     # with open(SAVE_FILENAME, "w", encoding="UTF-8") as filobj:
#         SAVE_FILENAME="Book_routine.obj"
#         with open(SAVE_FILENAME, "wb") as filobj:
#         # filobj.write(str(self.people))
#             pickle.dump(self, filobj)
#             filobj.close()
    
# class TreningsRutine(Book):
#     def __init__(self, tittel, reps, sets):
#         self.dato=datetime.utcnow
#         self.tittel=tittel
#         self.reps=reps
#         self.sets=sets
#     def __repr__(self):
#         return f"{self.dato}- {self.tittel}; {self.reps} x {self.sets}"
    
# class Controller(object):
#     def __init__(self):
#         self.book=self.load_obj()

#     def load_obj(self):
#         with open ("SAVE_FILENAME", "rb") as filobj:
#             book=pickle.load(filobj)
#             filobj.close()
#         return book

# a_book.save()


# kontroller = Controller()
# for personobjekt in kontroller.address_book.people:
#     print(personobjekt.first_name)
# # kontroller.address_book.
# print(kontroller.address_book)
        
        
## oppføring: dag - dato
## start tid, slutt tid
## øvelse
## reps, sets
## fler eller avslutt?
## evt notat?

