import csv
import StringIO
import zipfile
import time
import os

from django import http
from django.template import loader

from casam.models import Project, Measurement, OriginalImage
from casam.logic import export as export_logic
from casam.views import handler

class ExportHandler(handler.Handler):
  """
  """

  def get(self):
    project_id = self.kwargs['id_str']
    timestampedIDFilename = str(project_id) + '_' + str(time.time()) + '.zip'
    filepath = os.path.join('export',timestampedIDFilename)
    print filepath
    zip = zipfile.ZipFile(file=filepath,mode='w')
    export_script = export_logic.exportModels([Project, Measurement, OriginalImage], [Project], project_id)
    f = open('export_script.py', 'w')
    f.write(export_script)
    f.close()
    zip.write('export_script.py')
    zip.close()
    return http.HttpResponse('Saved file as %s' % timestampedIDFilename)


class CSVExportHandler(handler.Handler):
  """
  """

  def get(self):
    project_id = self.kwargs['id_str']
    project = Project.objects.get(id=project_id)
    measurements = Measurement.objects.filter(image__project=project)
    data = [dict(id=i.id, name=i.name(), x=i.x, y=i.y) for i in measurements]
    file_handler = StringIO.StringIO()
    key_order = ['id', 'name', 'x', 'y']

    writer = csv.DictWriter(file_handler, key_order, dialect='excel')

    header = dict((i, i) for i in key_order)

    writer.writerow(header)

    for row_dict in data:
      writer.writerow(row_dict)

    data = file_handler.getvalue()

    context = self.getContext()
    context['data'] = data
    content = loader.render_to_string('export.html', dictionary=context)
    content_type = 'text/csv'
    response = http.HttpResponse(content, mimetype=content_type)
    filename = project.name
    export_extension = ".csv"
    response['Content-Disposition'] = 'attachment; filename=%s%s' % (
        filename, export_extension)

    return response
