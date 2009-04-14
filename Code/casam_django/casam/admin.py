from django.contrib import admin
from casam.models import OriginalImage
from casam.models import WarpedImage
from casam.models import Patient

# new code will go here later on
admin.site.register(OriginalImage)
admin.site.register(WarpedImage)
admin.site.register(Patient)
