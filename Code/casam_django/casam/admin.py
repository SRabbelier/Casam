from django.contrib import admin
from models import OriginalImage
from models import ModifiedImage
from models import Project
from models import Tag

# new code will go here later on
admin.site.register(OriginalImage)
admin.site.register(ModifiedImage)
admin.site.register(Project)
admin.site.register(Tag)
