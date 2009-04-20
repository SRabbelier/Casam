from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

import casam.views.main
import casam.views.project
import casam.views.fileupload
import casam.views.landmarks

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', casam.views.main.home),
    (r'^project/new$', casam.views.project.new),
    (r'^project/(.*)$', casam.views.project.home),
    (r'^debug$', casam.views.main.debug),
    (r'^fileupload/(.*)$', casam.views.fileupload.fileupload),
    (r'^data/(.*)', casam.views.fileupload.viewfile),
    (r'^landmarks/save', casam.views.landmarks.save),
)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
