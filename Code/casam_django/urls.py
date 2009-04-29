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
import casam.views.user
import casam.views.login
import casam.views.draw
import casam.views.imageresizer
import casam.views.sjorsdraw

UUID = r"(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
USER_ID = r"(?P<user_id>[0-9]+)"
ID_STR = r"(?P<id_str>%s)" % UUID
IMG_NAME = r"(?P<img_name>[0-9a-zA-Z-./_]+)"

urlpatterns = patterns('',
    (r'^$', casam.views.main.Home()),
    (r'^admin/(.*)', admin.site.root),
    (r'^annotation/show/%s$' % UUID, casam.views.annotation.ViewAnnotation()),
    (r'^annotation/new/%s$' % UUID, casam.views.annotation.NewAnnotation()),
    (r'^annotation/list/%s$' % UUID, casam.views.annotation.ListAnnotations()),
    (r'^draw', casam.views.draw.Main()),
    (r'^data/%s' % IMG_NAME, casam.views.fileupload.ViewFile()),
    (r'^fileupload/%s$' % ID_STR, casam.views.fileupload.FileUpload()),
    (r'^landmarks/save', casam.views.landmarks.LandmarkSaver()),
    (r'^login', casam.views.login.Login()),
    (r'^logout', casam.views.login.Logout()),
    (r'^project/new$', casam.views.project.NewProject()),
    (r'^project/projectImagesJSON/(.*)$', casam.views.project.projectImagesJSON),
    (r'^project/%s$' % ID_STR, casam.views.project.Home()),
    (r'^resizeImage/byRatio/(.*)/(.*)$', casam.views.imageresizer.byRatio),
    (r'^resizeImage/byWidth/(.*)/(.*)$', casam.views.imageresizer.byWidth),
    (r'^sjorsdraw/AddBrushStroke$', casam.views.sjorsdraw.AddBrushStroke()),
    (r'^sjorsdraw$', casam.views.sjorsdraw.sjorsDraw()),
    (r'^user/home$', casam.views.user.Home()),
    (r'^user/new$', casam.views.user.CreateUser()),
    (r'^user/changepass/%s$' % USER_ID, casam.views.user.PassChange()),
    (r'^user/edit/%s$' % USER_ID, casam.views.user.EditUser()),
)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
