from django.contrib import admin
from models import OriginalImage
from models import WarpedImage
from models import Patient
from models import Project
from models import Department

# new code will go here later on
admin.site.register(OriginalImage)
admin.site.register(WarpedImage)
admin.site.register(Patient)
admin.site.register(Project)
admin.site.register(Department)
