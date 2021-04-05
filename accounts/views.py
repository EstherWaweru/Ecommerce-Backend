from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator
from .models import User
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


def home(request):
    return render(request,'home.html')
def demo(request):
    return render(request,'demo.html')

def signup(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            try:
                user=form.save(commit=False)
                user.is_active=False
                user.save()
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
            messages.error(request,form.errors)
            return HttpResponseRedirect(reverse("signup"))
    else:
        form=SignUpForm()
        return render(request,'accounts/signup.html',{'form':form})


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        #login user 
        #login(request,user)
        #return redirect ('home')
        #else:
        # return ('account/account_invalid.html')
        #toat success
        return HttpResponse('Thank you for ypur email confirmation.You can proceed to login to your account')
    else:
        #toast error on homepage
        return HttpResponse('Activation Link is invalid')





