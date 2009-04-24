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
import casam.views.draw
import casam.views.imageresizer
import casam.views.sjorsdraw

UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
ID_STR = r"(?P<id_str>%s)" % UUID
IMG_NAME = r"(?P<img_name>[0-9a-zA-Z-.]+)"

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', casam.views.users.Login()),
    (r'^do_login', casam.views.users.Login()),
    (r'^logout', casam.views.users.logout),    
    (r'^home', casam.views.main.Home()),
    (r'^project/projectImagesJSON/(.*)$', casam.views.project.projectImagesJSON),
    (r'^project/new$', casam.views.project.NewProject()),
    (r'^project/%s$' % ID_STR, casam.views.project.Home()),
    (r'^fileupload/%s$' % ID_STR, casam.views.fileupload.FileUpload()),
    (r'^data/%s' % IMG_NAME, casam.views.fileupload.ViewFile()),
    (r'^landmarks/save', casam.views.landmarks.LandmarkSaver()),
    (r'^user/new$', casam.views.users.Users()),
    (r'^user/home$', casam.views.users.home),
    (r'^user/save$', casam.views.users.Save()),
    (r'^user/(.*)$', casam.views.users.Edit()),
    (r'^resizeImage/byRatio/(.*)/(.*)$', casam.views.imageresizer.byRatio),
    (r'^resizeImage/byWidth/(.*)/(.*)$', casam.views.imageresizer.byWidth),
    (r'^draw', casam.views.draw.Main()),
    (r'^sjorsdraw', casam.views.sjorsdraw.sjorsDraw),
)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
