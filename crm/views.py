from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer, Order

# Create your views here.


def home(request):
    customers = Customer.objects.all()
    # Check to see if logging in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in!")
            return redirect('dashboard')
        else:
            messages.success(request, "There was an error logging in, please try aggain. . .")
            return redirect('home')
    else:
        return render(request, 'home.html', {'customers': customers})


def logout_user(request):
    # Log out the user 

    logout(request)
    messages.success(request, "You have logged out!")
    return redirect('home')


def dashboard(request):
    # See what's going on on the dashboard

    orders = Order.objects.all()
    return render(request, 'dashboard.html', {'orders': orders})


def customers_page(request):
    # Page for all customers

    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})


def change_status(request, pk):
    # Change order status

    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        if request.method == "POST":
            data = request.POST
            action = data.get("status")
            order.order_status = action.capitalize()
            order.save()
        return redirect('dashboard')


def transactions(request):
    # Show transactions page

    orders = Order.objects.filter(order_status='Finished')
    total = 0
    for order in orders:
        total += order.order_sum

    return render(request, 'transactions.html', {'orders': orders, 'total': f"{total:,}"})
