from django.conf import settings
from django import http
from django.template import loader

def sjorsDraw(request):
  content = loader.render_to_string('draw/sjorsdrawtest.html')
  
  return http.HttpResponse(content)
  
def addBrushStroke(request,brushStroke):
  user = request.user
  if user.is_authenticated():  
    
    wrapper = FileWrapper(file(temporaryImage))
    response = http.HttpResponse(wrapper, content_type='image/jpeg')
    response['Content-Length'] = os.path.getsize(temporaryImage)
  
    return response