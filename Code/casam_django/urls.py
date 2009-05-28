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
import casam.views.imageloader
import casam.views.bitmap_dump
import casam.views.tag
import casam.views.potential_measurement
import casam.views.pdm

UUID = r"(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
USER_ID = r"(?P<user_id>[0-9]+)"
ID_STR = r"(?P<id_str>%s)" % UUID
LOL = r"(?P<img_name>[0-9a-zA-Z-./_()]+)"
IMG_TYPE = r"(?P<img_type>original|bitmap)"
IMG_SIZE = r"(?P<img_size>[0-9]+)"
IMG_RATIO = r"(?P<img_ratio>(\+?((([0-9]+(\.)?)|([0-9]*\.[0-9]+))([eE][+-]?[0-9]+)?)))"
IMG_WIDTH = r"(?P<img_width>(\+?((([0-9]+(\.)?)|([0-9]*\.[0-9]+))([eE][+-]?[0-9]+)?)))"
IMG_HEIGHT = r"(?P<img_height>(\+?((([0-9]+(\.)?)|([0-9]*\.[0-9]+))([eE][+-]?[0-9]+)?)))"

urlpatterns = patterns('',
    (r'^$', casam.views.main.Home()),
    (r'^admin/(.*)', admin.site.root),
    (r'^annotation/show/%s$' % UUID, casam.views.annotation.ViewAnnotation()),
    (r'^annotation/new/%s$' % UUID, casam.views.annotation.NewAnnotation()),
    (r'^annotation/list/%s$' % UUID, casam.views.annotation.ListAnnotations()),
    (r'^data/%s' % LOL, casam.views.fileupload.ViewFile()),
    (r'^fileupload/%s$' % ID_STR, casam.views.fileupload.FileUpload()),
    (r'^landmarks/save', casam.views.landmarks.LandmarkSaver()),
    (r'^login', casam.views.login.Login()),
    (r'^logout', casam.views.login.Logout()),
    (r'^project/new$', casam.views.project.NewProject()),
    (r'^project/imageManager/%s$' % ID_STR, casam.views.project.ImageManager()),
    (r'^project/show/%s$' % ID_STR, casam.views.project.Home()),
    (r'^pm/new/%s$' % ID_STR, casam.views.potential_measurement.NewPotentialMeasurement()),
    (r'^pmt/new/%s$' % ID_STR, casam.views.potential_measurement.NewPotentialMeasurementType()),
    (r'^tag/new/%s$' % ID_STR, casam.views.tag.NewTag()),
    (r'^tag/select/%s$' % ID_STR, casam.views.tag.SelectTag()),
    (r'^imageLoader/byRatio/%s/%s/%s$' % (IMG_TYPE, IMG_RATIO, UUID), casam.views.imageloader.RatioHandler()),
    (r'^imageLoader/byWidth/%s/%s/%s$' % (IMG_TYPE, IMG_WIDTH, UUID), casam.views.imageloader.WidthHandler()),
    (r'^imageLoader/byMaxWidthHeight/%s/%s/%s/%s$' % (IMG_TYPE, IMG_WIDTH, IMG_HEIGHT, UUID), casam.views.imageloader.MaxWidthHeightHandler()),
    (r'^imageLoader/byMinWidthHeight/%s/%s/%s/%s$' % (IMG_TYPE, IMG_WIDTH, IMG_HEIGHT, UUID), casam.views.imageloader.MinWidthHeightHandler()),
    (r'^imageLoader/thumbnail/%s/%s/%s$' % (IMG_TYPE, IMG_SIZE, UUID), casam.views.imageloader.ThumbnailHandler()),
    (r'^imageLoader/%s/%s$' % (IMG_TYPE, UUID), casam.views.imageloader.SimpleHandler()),
    (r'^bitmap_dump$', casam.views.bitmap_dump.Save()),
    (r'^user/home$', casam.views.user.Home()),
    (r'^user/new$', casam.views.user.CreateUser()),
    (r'^user/changepass/%s$' % USER_ID, casam.views.user.PassChange()),
    (r'^user/edit/%s$' % USER_ID, casam.views.user.EditUser()),
    
    #JSON object loaders
    (r'^JSON/projects/(.*)$', casam.views.main.projectsJSON()),    
    (r'^JSON/projectImages/(.*)$', casam.views.project.projectImagesJSON),
    (r'^JSON/projectTags/(.*)$', casam.views.project.projectTagsJSON),
    (r'^JSON/projectAnnotations/(.*)$', casam.views.project.projectAnnotationsJSON),
    (r'^JSON/projectStates/(.*)$', casam.views.project.projectStatesJSON),
    (r'^JSON/projectPotentialMeasurements/(.*)$', casam.views.project.projectPotentialMeasurementsJSON),
    (r'^JSON/projectImageCurrentMeasurements/(.*)$', casam.views.project.projectImageCurrentMeasurementsJSON),
    (r'^JSON/projectImageBitmaps/(.*)$', casam.views.project.projectImageBitmapsJSON),
    (r'^JSON/userAuthenticated/$', casam.views.user.userAuthenticatedJSON),
    
    #AJaX Actions
    (r'^AJaX/deleteProjects/$', casam.views.main.deleteProjects()),
    (r'^AJaX/deleteImages/$', casam.views.main.deleteImages()),
    (r'^AJaX/deleteMeasurement/$', casam.views.main.deleteMeasurement()),
    (r'^AJaX/deletePotentialMeasurement/$', casam.views.main.deletePotentialMeasurement()),
    (r'^AJaX/deletePotentialMeasurementType/$', casam.views.main.deletePotentialMeasurementType()),
    (r'^AJaX/deleteAnnotations/$', casam.views.main.deleteAnnotations()),
    (r'^AJaX/addState/%s$' % UUID, casam.views.project.AddState()),

   #VTK
    (r'^vtk/PDMCreator$', casam.views.pdm.PDMCreator()),

)

if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^media/(.*)$', 'django.views.static.serve', {'document_root': 'media'}),
  )
