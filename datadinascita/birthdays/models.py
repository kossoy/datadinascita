from google.appengine.ext import db

# Create your models here.
class Person(db.Model):
    name = db.StringProperty(required=True)
    birthday = db.DateProperty()
    owner = db.UserProperty()