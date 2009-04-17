from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

import casam_django.casam.views.main
import casam_django.casam.views.fileupload

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', casam.views.main.home),
    (r'^fileupload$', casam.views.fileupload.fileupload),
    (r'^data/(.*)', casam.views.fileupload.viewfile)
)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
