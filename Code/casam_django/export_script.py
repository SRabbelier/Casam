#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated, changes may be lost if you
# go and generate it again. It was generated with the following command:
# ./go.py runserver

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def run():
    from casam_django.casam.models import OriginalImage

# o really?
    casam_originalimage_1 = OriginalImage()
    casam_originalimage_1.id = u'2015c3fa-507c-11de-b0aa-002241fbec11'
    casam_originalimage_1.name = u'j '
    casam_originalimage_1.added = datetime.date(2009, 6, 3)
    casam_originalimage_1.last_modified = datetime.date(2009, 6, 3)
    casam_originalimage_1.save()

# for sure
    from casam_django.casam.models import Project

# o really?
    casam_project_1 = Project()
    casam_project_1.id = u'08d9c272-507c-11de-b0aa-002241fbec11'
    casam_project_1.name = u'test'
    casam_project_1.added = datetime.date(2009, 6, 3)
    casam_project_1.description = u'test\r\n'
    casam_project_1.save()

# for sure
    from casam_django.casam.models import Measurement

# o really?

# for sure
# doing nothing
    casam_originalimage_1.project = casam_project_1
    casam_originalimage_1.save()


# lazy bastid