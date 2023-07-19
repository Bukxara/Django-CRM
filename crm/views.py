from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer, Order
from django.db.models import Sum

# Create your views here.


def home(request):
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
        return render(request, 'home.html')


def logout_user(request):
    # Log out the user 

    logout(request)
    messages.success(request, "You have logged out!")
    return redirect('home')


def dashboard(request):
    # See what's going on on the dashboard

    pending_orders = Order.objects.filter(status="Pending")
    in_progress_orders = Order.objects.filter(status="In Progress")
    on_delivery_orders = Order.objects.filter(status="On Delivery")
    orders = Order.objects.all()
    return render(request, "dashboard.html", {"orders": orders, "pending_orders": pending_orders, 
                        "in_progress_orders": in_progress_orders, "on_delivery_orders": on_delivery_orders})


def customers_page(request):
    # Page for all customers

    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})


def customer_orders(request, telegram_id):
    # Orders initiated by specific user

    customer_orders = Order.objects.filter(customer=telegram_id)
    total_revenue = customer_orders.filter(is_paid=True, is_refunded=False).aggregate(total_revenue=Sum("sum")).get("total_revenue")
    return render(request, "customer_orders.html", {"customer_orders": customer_orders, "total_revenue": total_revenue})


def change_status(request, pk):
    # Changes order's status to another

    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        if request.method == "POST":
            data = request.POST
            new_status = data.get("status").title()
            print(new_status)
            order.change_status(new_status)
        return redirect("dashboard")


def transactions(request):
    # Show transactions page

    paid_orders = Order.objects.filter(is_paid=True).order_by("-created_at")
    total_revenue = paid_orders.filter(is_refunded=False).aggregate(total=Sum("sum")).get("total")
    return render(request, "transactions.html", {"paid_orders": paid_orders, "total_revenue": total_revenue})
