from django import http
from casam.models import User

def handle_add_user(rlogin, rname, rtype, rid):
  user = User(login=rlogin, name=rname,type=rtype,password='12345', id=rid)
   
  user.save()
  #projid = uuid.UUID(post['read'])
  #pr = Project.objects.get(id=projid)
  #user.read.add(pr)
  #print user.read.all()
  #user.save()
  
def handle_login(username, password):  
  try:
    us = User.objects.filter(login=username).get()
    if us.password == password:
      return http.HttpResponseRedirect('home')
    else:
      return http.HttpResponseRedirect('.')
  except User.DoesNotExist:
    return http.HttpResponseRedirect('.')