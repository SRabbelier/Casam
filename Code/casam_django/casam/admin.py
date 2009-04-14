from django.contrib import admin
from models import OriginalImage
from models import WarpedImage
from models import Patient

# new code will go here later on
admin.site.register(OriginalImage)
admin.site.register(WarpedImage)
admin.site.register(Patient)
