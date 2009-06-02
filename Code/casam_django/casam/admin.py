from django.contrib import admin
from models import Project
from models import Tag
from models import Bitmap
from models import Measurement

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

admin.site.register(Bitmap,BitmapAdmin)
admin.site.register(Measurement,MeasurementAdmin)
admin.site.register(Project)
admin.site.register(Tag)

