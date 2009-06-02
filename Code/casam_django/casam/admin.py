from django.contrib import admin
from models import Project
from models import Tag
from models import Bitmap
from models import Measurement
from models import PDM

# new code will go here later on
class MeasurementAdmin(admin.ModelAdmin):
  list_select_related = True
  list_display = ('project','image','type','mogelijkemeting')
  list_filter = ['image','mogelijkemeting']
  fields = ['image']

class BitmapAdmin(admin.ModelAdmin):
  list_select_related = True
  list_display = ('project','image','type','mogelijkemeting')
  list_filter = ['image','mogelijkemeting']
  fields = ['image']

class PDMAdmin(admin.ModelAdmin):
  list_select_related = True
  list_display = ('project','added')
  list_filter = ['project']
  fields = ['name']

admin.site.register(Bitmap,BitmapAdmin)
admin.site.register(Measurement,MeasurementAdmin)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(PDM, PDMAdmin)

