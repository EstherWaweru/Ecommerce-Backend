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
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
import requests
import json
from django.http import JsonResponse



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
                # try:
                user=authenticate(email=email,password=password)
                # except Exception as e:
                #     traceback.print_exc()
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
    print(result)
    return result





    







