from django import http
from django.contrib.auth import authenticate, login, logout

from casam.models import UserProfile
from casam.models import Project

from django.contrib.auth.models import User, Group

def handle_add_user(rlogin, rfirstname, rlastname, rpass, rtype, read_projs):
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
    profile = user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile(user=user)
    profile.save()
    
  projid = read_projs[:-2]
  projid = projid[3:]
  pr = Project.objects.get(id=projid)
  profile.read.add(pr)
  profile.save()  
  
  for projid in read_projs:
    print projid
    try:
      pr = Project.objects.get(id=projid)
      profile.read.add(pr)
    except Project.DoesNotExist:
      pass
    #up = user.get_profile()  
  
  user.save()
    
  try:
    utype = Group.objects.get(name=gtype)
    user.groups.add(utype)
    user.save()
  except Group.DoesNotExist:
    print 'Group does not exist'    
  
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
  
def handle_edit(rfirst_name, rlast_name, rtype, rid):
  user = User.objects.get(id=rid)
  user.first_name = rfirst_name
  user.last_name = rlast_name
  user.save()
  
  if rtype == 'C':
    gtype = 'Chirurg'
  elif rtype == 'O':
    gtype = 'Onderzoeker'
  else:
    gtype = 'Beheerder'  
  
  gr1 = Group.objects.get(name=gtype)
  user.groups.clear()
  user.groups.add(gr1)
  user.save()  
    
  return http.HttpResponseRedirect('./home')           

def handle_logout(request):
  logout(request)
  return http.HttpResponseRedirect('./')         