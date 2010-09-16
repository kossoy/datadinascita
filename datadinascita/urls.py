from django.conf.urls.defaults import *
from datadinascita.birthdays import views

urlpatterns = patterns('',
    (r'^$', views.list),
    (r'^people/$', views.list),
    (r'^add/$', views.add)
    # Example:
    # (r'^datadinascita/', include('datadinascita.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
