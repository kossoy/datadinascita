from django.conf.urls.defaults import *

urlpatterns = patterns('datadinascita.birthdays.views',
   (r'^$', 'list'),
   (r'^people/$', 'list'),
   (r'^add/$', 'add'),
   (r'^erase/$', 'erase'),
   (r'^search/$', 'search'),
   (r'^import/$', 'csv_upload'),
   (r'^export/$', 'export'),
   (r'^test/$', 'test'),
   (r'^upload/$', 'upload_photo'),
)
