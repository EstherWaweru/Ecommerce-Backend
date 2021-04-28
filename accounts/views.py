from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.contrib.auth.models import Group,Permission
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
import traceback
from django.core import serializers
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
import requests
import json
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.db.models import Count




def home(request):
    return render(request,'home.html')
def demo(request):
    return render(request,'demo.html')

def signup(request):
    '''
    customer registration 
    '''
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            result=recaptcha_validation(request)
            if result['success']:
                try:
                    user=form.save(commit=False)
                    user.is_active=False
                    user.save()
                    role=Group.objects.get('Customer')
                    role.user_set.add(user)
                    current_site=get_current_site(request)
                    mail_subject='Activate your account'
                    context1={'user':user,
                            'domain':current_site.domain,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':default_token_generator.make_token(user)
                            }
                    message=render_to_string('accounts/account_activation_email.html',context1)
                    email_from = settings.EMAIL_HOST_USER
                    to_email=form.cleaned_data.get('email')
                    email=EmailMessage(mail_subject,message,email_from,[to_email])
                    email.send(fail_silently=False)
                    messages.success(request,'Success.Please confirm your email address to complete registration')
                    return HttpResponseRedirect(reverse("signup"))
                except Exception as e:
                    traceback.print_exc()
                    messages.error(request,e)
                    return HttpResponseRedirect(reverse("signup"))  
            else: 
                messages.error(request,'Invalid reCAPTCHA. Please try again.')
                return HttpResponseRedirect(reverse("signup"))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse("signup"))
    else:
        form=SignUpForm()
        return render(request,'accounts/signup.html',{'form':form,'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return redirect ('home')
        messages.success(request,'Email confirmation successful!')
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.error(request,'Activation Link is Invalid')
        return HttpResponseRedirect(reverse('signup'))
def user_login(request):
    '''
    User login with email and password
    '''
    if request.method=='POST':
        form=LoginForm(request.POST)
        #recaptcha validation
        
        if form.is_valid():
            result=recaptcha_validation(request)
            if result['success']:
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                remember_me=form.cleaned_data['remember_me']
                user=authenticate(email=email,password=password)
                if user!=None:
                    login(request,user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request,'Invalid email or password!')
                    return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.error(request,result['error-codes'])
                return HttpResponseRedirect(reverse('user_login'))
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse('user_login'))
    else:
        form=LoginForm()
        return render(request,'accounts/login.html',{'form':form,'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

def user_logout(request):
    logout(request)
    #to do 
    # create a landing page and redirect to that instead
    return HttpResponseRedirect(reverse('user_login'))

def recaptcha_validation(request):
    '''
    Validate recaptcha site key with the secret key
    '''
    recaptcha_response=request.POST.get('g-recaptcha-response')
    data={
    'secret':settings.GOOGLE_RECAPTCHA_SECRET_KEY,
    'response':recaptcha_response}
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result=r.json()
    return result
@login_required
def dashboard(request):
    '''
    Admins dashboard
    TODO:Add a group required decoration
    '''
    return render(request,'dashboard.html')
@login_required
def roles(request):
    group_list=Group.objects.all()
    context={'groups':group_list}
    return render(request,'accounts/roles.html',context)
def role_view(request,group_id):
    #to do display roles and permissions using ajax
    context={'group_id':group_id}
    return render(request,'accounts/roles.html',context)
def role_view_ajax(request):
    if request.method=='POST':
        group_id=request.POST.get("group_id")
        group=Group.objects.get(id=group_id)
        permissions=group.permissions.all()
        data={'group':group.name,'permissions':list(permissions.values())}
        return JsonResponse(data)
    else:
        return render(request,'accounts/roles.html',context)
def create_group_ajax(request):
    if request.method=='POST':
        group_name=request.POST.get("role_name")
        perms=request.POST.getlist('perms[]')
        permissions_ids=[int(id) for id in perms]
        new_group,created=Group.objects.get_or_create(name=group_name)
        permission_list=[]
        for id in permissions_ids:
            permission=Permission.objects.get(id=id)
            permission_list.append(permission)
        new_group.permissions.set(permission_list)
        messages.success(request,"Group created successfuly!")
        data={'status':"Group created successfuly!"}
        return JsonResponse(data)
    else:
        messages.error(request,"Failed to create a Group")
        return render(request,'accounts/roles.html')

def edit_group_ajax(request):
    if request.method=='POST':
        group_id=request.POST.get('group_id')
        group=Group.objects.get(id=group_id)
        all_permissions=Permission.objects.all()
        serialized_obj = serializers.serialize('json', [ group, ])
        struct = json.loads(serialized_obj)
        data1 = json.dumps(struct[0])
        dict_obj = model_to_dict( group )
        perm=dict_obj.pop('permissions')
        new_data=serializers.serialize('json', perm,fields=('name','codename'))
        dict_obj['permissions']=json.loads(new_data)
        dict_obj['all_permissions']=list(all_permissions.values())
        return JsonResponse(dict_obj)
    else:
        return render(request,"accounts/roles.html")
def ajax_edit_role(request):
    if request.method=='POST':
        group_id=request.POST.get("role_id")
        group_name=request.POST.get("group_name")
        ids_values=request.POST.getlist("arrValue[]")
        ids_count=len(ids_values)
        group=Group.objects.get(id=group_id)
        group.name = group_name
        group.save()
        all_permissions_count=Permission.objects.all().count()
        all_permissions=Permission.objects.all()
        permission_ids= [int(id) for id in ids_values]
        if ids_count==all_permissions_count:
            group.permissions.clear()
            group.permissions.set(list(set(all_permissions)))
        elif ids_count==0:
            group.permissions.clear()
        else:
            group.permissions.clear()
            permission_list=[]
            for perm in permission_ids:
                permission=Permission.objects.get(id=perm)
                permission_list.append(permission)
            group.permissions.set(permission_list)
        messages.success(request,"Succesfuly Edited")
        return JsonResponse({'status':'Success Roles Update!'})
    else:
        return render(request,'accounts/roles.html')
def create_role(request):
    if request.method=='GET':
        all_permissions=Permission.objects.all()
        data={'all_permissions':list(all_permissions.values())}
        return JsonResponse(data)
    else:
        return render(request,"accounts/roles.html")        
def delete_group_ajax(request):
    try:
        id=request.POST.get("id")
        group=Group.objects.get(id=id)
        group.delete()
        messages.success(request,"Successfully Deleted Group")
        return JsonResponse({'status':"Successfuly Deleted a Group"})
    except:
        messages.error(request,"Failed to Delete Group ")
        return HttpResponse("False")
def permissions_list(request):
    permissions=Permission.objects.all().values('name','id','codename')
    context={'permissions':permissions}
    return render(request,'accounts/permissions.html',context)
def add_permission(request):
    if request.method=='POST':
        permission_name=request.POST.get("permission_name")
        permission_codename=request.POST.get("permission_codename")
        if len(permission_name)>0 and len(permission_codename)>0:
            userct = ContentType.objects.get_for_model(User)
            created_permission = Permission.objects.create(codename =permission_codename, name =permission_name, content_type = userct)
        messages.success(request,"Permissions created successfuly!")
        data={'status':"Permissions created successfuly!"}
        return JsonResponse(data)
    else:
        messages.error(request,"Failed to create a Permmissions")
        return render(request,'accounts/permissions.html')
def delete_permission_ajax(request):
    try:
        id=request.POST.get("id")
        permission=Permission.objects.get(id=id)
        permission.delete()
        messages.success(request,"Successfully Deleted Permission")
        return JsonResponse({'status':"Successfuly Deleted a Permission"})
    except:
        messages.error(request,"Failed to Delete A Permission ")
        return HttpResponse("False")

        


    
   









    







