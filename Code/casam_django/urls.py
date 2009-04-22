from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

import casam.views.main
import casam.views.project
import casam.views.fileupload
import casam.views.landmarks
import casam.views.users

UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
ID_STR = r"(?P<id_str>%s)" % UUID

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', casam.views.users.Login()),
    (r'^do_login', casam.views.users.Login()),
    (r'^home', casam.views.main.Home()),
    (r'^project/projectImagesJSON/(.*)$', casam.views.project.projectImagesJSON),
    (r'^project/new$', casam.views.project.NewProject()),
    (r'^project/%s$' % ID_STR, casam.views.project.Home()),
    (r'^fileupload/%s$' % ID_STR, casam.views.fileupload.FileUpload()),
    (r'^data/(.*)', casam.views.fileupload.viewfile),
    (r'^landmarks/save', casam.views.landmarks.LandmarkSaver()),
    (r'^user/new$', casam.views.users.Users()),
    (r'^user/home$', casam.views.users.home),
    (r'^user/(.*)$', casam.views.users.view)
)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
