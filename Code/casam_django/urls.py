from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import casam_django.casam.views.main
import casam_django.casam.views.fileupload

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', casam_django.casam.views.main.home),
    (r'^fileupload$', casam_django.casam.views.fileupload.fileupload),
    (r'^data/(.*)', casam_django.casam.views.fileupload.viewfile),
)
