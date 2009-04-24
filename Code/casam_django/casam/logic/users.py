from django import http
from django.contrib.auth import authenticate, login, logout

from casam.models import UserProfile
from casam.models import Project

from django.contrib.auth.models import User, Group

def handle_add_user(rlogin, rfirstname, rlastname, rpass, rtype, read_projs, write_projs):
  rname = rfirstname+' '+rlastname
  
  user = User.objects.create_user(rlogin,'',rpass)
  user.first_name = rfirstname
  user.last_name = rlastname
  user.is_staff = True
  user.set_password(rpass)
  
  try:
    profile = user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile(user=user)
    profile.save()
  
  for proj in read_projs:
    try:
      profile.read.add(proj)
      profile.save()
    except Project.DoesNotExist:
      pass
    
  for proj in write_projs:
    try:
      profile.write.add(proj)
      profile.save()
    except Project.DoesNotExist:
      pass    
  
  user.save()
    
  try:
    user.groups.add(rtype)
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
  
def handle_edit(rfirst_name, rlast_name, rtype, rid, rread, rwrite):
  user = User.objects.get(id=rid)
  user.first_name = rfirst_name
  user.last_name = rlast_name
  user.save()
  
  gtype = ''
  for gr in Group.objects.all():
    if gr.id == int(rtype):
      gtype = gr.name
      break  
  
  gr1 = Group.objects.get(name=gtype)
  user.groups.clear()
  user.groups.add(gr1)
  user.save()  
  
  try:
    profile = user.get_profile()
    for projid in rread:
      profile.read.clear()
      profile.save()
      try:
        proj = Project.objects.get(id=projid)
        profile.read.add(proj)
        profile.save()
      except Project.DoesNotExist:
        pass
      
      print profile.read.all()
      
    for projid in rwrite:
      profile.write.clear()
      profile.save()
      try:
        proj = Project.objects.get(id=projid)
        profile.write.add(proj)
        profile.save()
      except Project.DoesNotExist:
        pass
      
    profile.save()
  except UserProfile.DoesNotExist:
    pass
  
  user.save()   
    
  return http.HttpResponseRedirect('./home')           

def handle_logout(request):
  logout(request)
  return http.HttpResponseRedirect('./')         

def handle_pass_change(rlogin, rpass1, rpass2, rid):
  user = User.objects.get(id=rid)
  if rpass1 == rpass2:
    user.set_password(rpass1)
    return True
  else:
    return False
  