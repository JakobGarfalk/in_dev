class Crapper(object):
    def __init__(self, app=None, db=None):
        self.app=app
        self.purpose=[1,2,3,4,5,6,7,8]
        if not app==None:
            self.init_crap(app, db)

    def init_app(self, app, db):
        app.crapper=self
        self.db=db
    
# ved å binde et objekt til flask instans, & koble på db etter instans av dette,
# bør Crapper kunne ha mulighet til:
# å være et globalt objekt, oppbevarer hva som helst og har request context
#(ihvertfall) app_context. 