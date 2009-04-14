from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import views.main

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', views.main.home),
)
