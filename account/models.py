from mongoengine import *
# Create your models here.
connect('TrustNews')


class User(DynamicDocument):
    username = StringField()
    permission = StringField()  # user, manager, admin
    # password, nickname, public_key, private_key, profile_picture, email...
    # all thing above are not basic info of a user, working on it later
    #
    #
    # ----------------------- we will add them later ------------------------


    def __unicode__(self):
        return self.username
