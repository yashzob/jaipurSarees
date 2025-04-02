from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
import random
import uuid  # Import UUID
from .helper import MessageHandler
from twilio.rest import Client

account_sid = 'ACce22acc627a519261fa51a50bd0e990b'
auth_token = '491bc38db133afa3e708d333dd36d680'
client = Client(account_sid, auth_token)

def home(request):
    if request.COOKIES.get('verified') and request.COOKIES.get('verified') != None:
        return HttpResponse(" verified.")
    else:
        return HttpResponse(" Not verified.")

def generate_unique_uid():
    while True:
        uid = str(uuid.uuid4())  # Generate a unique UUID for the uid
        if not Profile.objects.filter(uid=uid).exists():
            return uid

def register(request):
    print("request")
    if request.method == "POST":
        if User.objects.filter(username__iexact=request.POST['user_name']).exists():
            return HttpResponse("User already exists")

        user = User.objects.create(username=request.POST['user_name'])
        otp = random.randint(1000, 9999)
        print(otp)

        # Ensure unique uid using UUID
        uid = generate_unique_uid()  # Generate a unique UID
        profile = Profile.objects.create(user=user, phone_number=request.POST['phone_number'], otp=f'{otp}', uid=uid)

        if request.POST['methodOtp'] == "methodOtpWhatsapp":
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=f'Your OTP is: {otp}',  # Send the OTP in the message body
                to=f'whatsapp:{request.POST["phone_number"]}'
            )
        
        red = redirect('otp', uid=profile.uid)  # Use the URL name for redirection
        red.set_cookie("can_otp_enter", True)
        return red  
    return render(request, 'register.html')

def otpVerify(request, uid):
    print("otpppppppppppppppppppppppppppppppppppppppppp", uid)
    print(request)
    if request.method == "POST":
        profile = Profile.objects.get(uid=uid)
        print("OTP for verification:", profile.otp)     
        print("Received OTP from form:", request.POST['otp'])  # Debugging statement to check the submitted OTP


        if request.COOKIES.get('can_otp_enter') != None:
            if profile.otp == request.POST['otp']:
                
                red = redirect("store")# reditct to store\templates\store\store.html
                red.set_cookie('verified', True)
                print("Done")
                return red
            return HttpResponse("wrong otp")
        return HttpResponse("10 minutes passed")        
    return render(request, "otp.html", {'id': str(uid)})

def test(request):
    return render(request, 'test.html')
