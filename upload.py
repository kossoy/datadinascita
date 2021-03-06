from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from datadinascita.birthdays.models import Person

import logging
from google.appengine.ext.blobstore.blobstore import fetch_data
from StringIO import StringIO
import csv
from datetime import datetime


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload_files = self.get_uploads('file')
            blob_info = upload_files[0]
            if blob_info.size > 1048576:
                self.redirect('/upload_failure')

            csv_file = fetch_data(blob_info, 0, blob_info.size + 1)
            stringReader = csv.reader(StringIO(csv_file))

            for row in stringReader:
                logging.info(row)
                p = Person(name=row[1].decode('utf-8'))
                p.owner = users.get_current_user()
                p.birthday = datetime.date(datetime.strptime(row[0], "%m/%d/%Y"))
                p.put()

            self.redirect('/')
        except:
            self.redirect('/upload_failure/')

class fail(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
            <html>
            <body>
                <h1 style="color: Red;">Failed</h1>
                <p>Possibly, file is too big or not csv ('12/31/1970', 'Person name'\r\n, etc)</p>
                <a href="/import/">Try again</a>
            <body>
            <html>
                                ''')

class test(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Test')

application = webapp.WSGIApplication([
                                             ('/upload_csv/', UploadHandler),
                                             ('/test/', test),
                                             ('/upload_failure/', fail),
                                             ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
