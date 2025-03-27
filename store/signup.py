from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer  # Import the Customer model


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return render(request, 'store/signup.html', {'error': 'Username already exists'})

            if User.objects.filter(phone=phone).exists():
                return render(request, 'store/signup.html', {'error': 'Phone number already registered'})

            user = User.objects.create_user(username=username, password=password)

            # Create the Customer instance and associate it with the user
            customer = Customer.objects.create(user=user, phone=phone)

            return redirect('store/main')  # Replace 'success' with the name of your success page or URL

        else:
            return render(request, 'store/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'store/signup.html')