from google.appengine.ext import db
from google.appengine.ext import blobstore

# Create your models here.
class Person(db.Model):
    name = db.StringProperty(required=True)
    birthday = db.DateProperty()
    owner = db.UserProperty()

class PhotoItem(db.Model):
    name = db.StringProperty()
    photo = blobstore.BlobReferenceProperty()