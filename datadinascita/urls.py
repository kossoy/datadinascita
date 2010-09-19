from django.conf.urls.defaults import *

urlpatterns = patterns('datadinascita.birthdays.views',
   (r'^$', 'list'),
   (r'^people/$', 'list'),
   (r'^add/$', 'add'),
   (r'^search/$', 'search'),
   (r'^import/$', 'csv_upload'),
   (r'^test/$', 'test'),
)
