from django import http
from django.contrib.auth import authenticate, login

from casam.models import UserProfile

from django.contrib.auth.models import User, Group

def handle_add_user(rlogin, rfirstname, rlastname, rpass, rtype):
  rname = rfirstname+' '+rlastname
  
  if rtype == 'C':
    gtype = 'Chirurg'
  elif rtype == 'O':
    gtype = 'Onderzoeker'
  else:
    gtype = 'Beheerder'
  
  user = User.objects.create_user(rlogin,'',rpass)
  user.first_name = rfirstname
  user.last_name = rlastname
  user.is_staff = True
  user.set_password('12345')
  
  try:
    user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile(user=user)
    profile.save()
    #up = user.get_profile()  
  
  user.save()
    
  try:
    utype = Group.objects.get(name=gtype)
    user.groups.add(utype)
    user.save()
  except Group.DoesNotExist:
    print 'Group does not exist'
    
  
  #pr = Project.objects.get(id=projid)
  #user.read.add(pr)
  #print user.read.all()
  #user.save()
  
def handle_login(request):
  rusername = request.POST['username']
  rpassword = request.POST['password']
  user = authenticate(username=rusername, password=rpassword)                 
  if user is not None:
    if user.is_active:
      login(request, user)
      return http.HttpResponseRedirect('home')
    else:
      return http.HttpResponseRedirect('.')
  else:
    return http.HttpResponseRedirect('.')                     