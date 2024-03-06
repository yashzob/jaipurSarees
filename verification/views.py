from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profile
import random
from .helper import MessageHandler

def home(request):
        if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
            return HttpResponse(" verified.")
        else:
            return HttpResponse(" Not verified.")

def register(request):
    print("request")
    if request.method=="POST":
        if User.objects.filter(username__iexact=request.POST['user_name']).exists():
            return HttpResponse("User already exists")

        user=User.objects.create(username=request.POST['user_name'])
        otp=random.randint(1000,9999)
        print(otp)
        profile=Profile.objects.create(user=user,phone_number=request.POST['phone_number'],otp=f'{otp}')
        if request.POST['methodOtp']=="methodOtpWhatsapp":
            messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_whatsapp()
        red=redirect(f'otp/{profile.uid}/')
        red.set_cookie("can_otp_enter",True)
        return red  
    return render(request, 'ver/register.html')

def otpVerify(request,uid):
    print("otpppppppppppppppppppppppppppppppppppppppppp",uid)
    if request.method=="POST":
        profile=Profile.objects.get(uid=uid)     
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==request.POST['otp']):
                red=redirect("home")
                red.set_cookie('verified',True)
                return red
            return HttpResponse("wrong otp")
        return HttpResponse("10 minutes passed")        
    return render(request,"otp.html",{'id':uid})
   
from uuid import uuid4
def register(request):
    from django.db import models
    if request.method=="POST":
        if User.objects.filter(username__iexact=request.POST['user_name']).exists():
            return HttpResponse("User already exists")

        user=User.objects.create(username=request.POST['user_name'])
        otp=random.randint(1000,9999)
        print("otp")
        profile=Profile.objects.create(user=user,phone_number=request.POST['phone_number'],otp=f'{otp}')
        if request.POST['methodOtp']=="methodOtpWhatsapp":
            messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_whatsapp()
        else:
            messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
        
        
        print("Profile UID:", profile.uid)
        #red=redirect(f'otp/{profile.uid}/')
        #red = redirect(f'/ver/otp/{profile.uid}/')
        red = redirect('otp', uid=profile.uid)
  # Assuming /ver/ is the correct URL prefix
        print("heelooo")

        red.set_cookie("can_otp_enter",True,max_age=600)
        return red  
    return render(request, 'register.html')

def test(request):
    return render(request, 'test.html')

