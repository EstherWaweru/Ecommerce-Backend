from django.shortcuts import render,redirect
from .forms import SignUpForm
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string




# Create your views here.
def signup(request):
    if request.method=='GET':
        render(request,'accounts/signup.html')
    if request.method=='POST':
        form=SignUpForm(request.POST)
    # print(form.errors.as_data())
        if form.is_valid():
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
            to_email=form.cleaned_data.get('email')
            email=EmailMessage(mail_subject,message,to_email)
            email.send()
            print("mail**********************")
        return HttpResponse("Please confirm your email address to complete registration")
    else:
        form=SignUpForm()
        return render(request,'accounts/signup.html',{'form':form})

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
        print("user******",user)
    except(TypeError,ValueError,OverflowError,User.DoestNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        #login user 
        #login(request,user)
        #return redirect ('home')
        #else:
        # return ('account/account_invalid.html')

        return HttpResponse('Thank you for ypur email confirmation.You can proceed to login to your account')
    else:
        return HttpResponse('Activation Link is invalid')





