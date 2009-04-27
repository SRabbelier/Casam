from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

import casam.views.main
import casam.views.annotation
import casam.views.project
import casam.views.fileupload
import casam.views.landmarks
import casam.views.users
import casam.views.draw
import casam.views.imageresizer
import casam.views.sjorsdraw

UUID = r"(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
ID_STR = r"(?P<id_str>%s)" % UUID
IMG_NAME = r"(?P<img_name>[0-9a-zA-Z-./_]+)"

urlpatterns = patterns('',
    (r'^$', casam.views.users.Login()),
    (r'^admin/(.*)', admin.site.root),
    (r'^annotation/show/%s$' % UUID, casam.views.annotation.ViewAnnotation()),
    (r'^annotation/new/%s$' % UUID, casam.views.annotation.NewAnnotation()),
    (r'^annotation/list/%s$' % UUID, casam.views.annotation.ListAnnotations()),
    (r'^data/%s' % IMG_NAME, casam.views.fileupload.ViewFile()),
    (r'^do_login', casam.views.users.Login()),
    (r'^draw', casam.views.draw.Main()),
    (r'^fileupload/%s$' % ID_STR, casam.views.fileupload.FileUpload()),
    (r'^home', casam.views.main.Home()),
    (r'^landmarks/save', casam.views.landmarks.LandmarkSaver()),
    (r'^logout', casam.views.users.logout),
    (r'^project/new$', casam.views.project.NewProject()),
    (r'^project/projectImagesJSON/(.*)$', casam.views.project.projectImagesJSON),
    (r'^project/%s$' % ID_STR, casam.views.project.Home()),
    (r'^resizeImage/byRatio/(.*)/(.*)$', casam.views.imageresizer.byRatio),
    (r'^resizeImage/byWidth/(.*)/(.*)$', casam.views.imageresizer.byWidth),
    (r'^sjorsdraw/AddBrushStroke$', casam.views.sjorsdraw.AddBrushStroke()),
    (r'^sjorsdraw$', casam.views.sjorsdraw.sjorsDraw()),
    (r'^user/home$', casam.views.users.Home()),
    (r'^user/new$', casam.views.users.Users()),
    (r'^user/save$', casam.views.users.Save()),
    (r'^user/changepass$', casam.views.users.PassChange()),
    (r'^user/change$', casam.views.users.Change()),
    (r'^user/(.*)$', casam.views.users.Edit()),
)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
