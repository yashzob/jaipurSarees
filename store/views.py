from django.shortcuts import render, get_object_or_404
from .models import Product  # Assuming Product is the model for your products

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})
from .models import * 
from django.http import JsonResponse

from django.contrib.auth.forms import UserCreationForm
import json
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



    #def clean_phone(self):
    #    phone = self.cleaned_data['phone']
    #    if User.objects.filter(phone=phone).exists():
    #        raise forms.ValidationError("This phone number is already registered.")
    #    return phone




def store(request):
    products = Product.objects.all()
    
    total_quantity = request.session.get('total_quantity', 0)  # Retrieve total_quantity from session
    
    context = {'products': products, 'total_quantity': total_quantity}
    
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        total_cost = 0
        total_quantity = 0

        for item in items:
            total_quantity += item.quantity
            item.total_price = item.product.price * item.quantity
            total_cost += item.total_price
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        total_cost = 0
        total_quantity = 0
    
    request.session['total_quantity'] = total_quantity
    request.session['total_cost'] = total_cost
    request.session.modified = True  # Mark the session as modified

    context = {'items': items, 'order': order, 'total_cost': total_cost, 'total_quantity': total_quantity}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    total_quantity = request.session.get('total_quantity', 0)
    total_cost = request.session.get('total_cost', 0)

    context = {'items': items, 'order': order, 'total_quantity': total_quantity, 'total_cost': total_cost}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        if request.user.is_authenticated:
            customer = request.user.customer
            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                orderItem.quantity = (orderItem.quantity + 1)
            elif action == 'remove':
                orderItem.quantity = (orderItem.quantity - 1)

            orderItem.save()

            if orderItem.quantity <= 0:
                orderItem.delete()

            return JsonResponse('Item was updated', safe=False)
        else:
            return JsonResponse('User is not authenticated', status=401)
    else:
        return JsonResponse('Invalid request method', status=400)

from django.shortcuts import render
from .models import ShippingAddress

def save_shipping_address(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        if not all([name, email, address, city, state, zipcode]):
            messages.error(request, 'Please fill all required fields')
            return redirect('checkout')

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            customer = None
            order = None

        shipping_address = ShippingAddress(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode
        )
        shipping_address.save()
        
        # Store name and email in session since they're not in ShippingAddress model
        request.session['customer_name'] = name
        request.session['customer_email'] = email

        if payment_method == 'stripe':
            return redirect('payment')
        elif payment_method == 'cod':
            return process_cod(request, order, shipping_address)
        else:
            messages.error(request, 'Invalid payment method')
            return redirect('checkout')

def process_cod(request, order, shipping_address):
    if order:
        order.complete = True
        order.save()
    
    # Store order details in session for guest users
    if not request.user.is_authenticated:
        request.session['order_id'] = order.id if order else None
        request.session['shipping_address_id'] = shipping_address.id
        request.session.modified = True
    
    # Create order confirmation
    context = {
        'order': order,
        'shipping_address': shipping_address,
        'payment_method': 'Cash on Delivery',
        'customer_name': request.session.get('customer_name', ''),
        'customer_email': request.session.get('customer_email', '')
    }
    return render(request, 'store/order_confirmation.html', context)

# views.py

#from django.conf import settings
#from django.shortcuts import render
#import stripe

#stripe.api_key = settings.STRIPE_SECRET_KEY

#from django.shortcuts import render
# import stripe
# from django.conf import settings

def payment(request):
    if request.method == 'POST':
        # Tokenize and process the payment
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=.1,  # Amount in cents
                currency='inr',
                description='Example Charge',
                source=token,
            )
            # Payment successful
            return render(request, 'payment/success.html')
        except stripe.error.CardError as e:
            # Payment failed
            return render(request, 'payment/error.html', {'error': e.error.message})
    else:
        # Render the payment form
        context = {'publishable_key': settings.STRIPE_PUBLISHABLE_KEY}
        return render(request, 'payment/form.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .models import Customer

def login1(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Check if the user already exists in the database (using email as username)
        existing_user = User.objects.filter(email=username_or_email).first()

        if existing_user:
            # User already exists, try authenticating the user
            user = authenticate(request, username=existing_user, password=password)
        else:
            # User does not exist, register a new user
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
            else:
                # Handle invalid form data
                messages.error(request, 'Invalid registration data.')
                return render(request, 'store/login.html', {'form': form})

        if user is not None:
            # Login the user and redirect to the store page
            login(request, user)

            # Create a related Customer record if it doesn't exist already
            customer, created = Customer.objects.get_or_create(user=user, email=user.email)
            if created:
                # You can add additional fields to the Customer model here
                customer.name = user.username
                customer.save()

            return redirect('store')  # Replace 'store' with the name of your store page or URL
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username/email or password.')

    form = CustomUserCreationForm()  # Create an empty form for GET requests
    return render(request, 'store/login.html', {'form': form})


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField()
    #phone_number= "+91" + phone_number

    class Meta:
        model = User
        fields = ['username', 'email',  'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

from django.shortcuts import render, redirect

from .models import Customer

def register(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the User object first

            # Retrieve cleaned data from the form
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            
            # Create a Customer instance and associate it with the User
            customer = Customer.objects.create(user=user, email=email, phone_number=phone_number)
            customer.name = user.username  # Set the name to the username by default
            customer.save()

            # You can also use the 'login' function to log in the user automatically
            # after registration if you wish to do so
            # login(request, user)

            # Redirect the user to a success page or wherever you want
            return redirect('store/login.html')  # Replace 'success' with your desired URL
        else:
            print("invalid details filled")

    context = {'form': form}
    return render(request, 'store/register.html', context)



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')
