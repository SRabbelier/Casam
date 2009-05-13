import csv
import StringIO

from django import http
from django.template import loader

from casam.views import handler

class ExportHandler(handler.Handler):
    """
    """

    def get(self):
        data = {}
        key_order = []
        file_handler = StringIO.StringIO()
        key_order = []

        writer = csv.DictWriter(file_handler, key_order, dialect='excel')

        header = dict((i, i) for i in key_order)

        writer.writerow(header)

        for row_dict in data:
            writer.writerow(row_dict)

        data = file_handler.getvalue()

        context = self.getContext()
        context['data'] = data
        content = loader.render_to_string('export.html', dictionary=context)
     
        response = http.HttpResponse(content, mimetype=content_type)
     
        response['Content-Disposition'] = 'attachment; filename=%s%s' % (
            filename, export_extension)

        return response
