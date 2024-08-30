from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from .models import Product, Order, Supplier, User
from .forms import RegistrationForm, LoginForm
import plotly.express as px
from plotly.offline import plot

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.role = role
            user.set_password(form.cleaned_data['password1'])  # Ensure password is hashed
            user.save()
            auth_login(request, user)  # Automatically log the user in after registration
            print(f"Registered user: {user.username}, role: {user.role.name}")  # Debugging line
            return redirect_user_based_on_role(user)  # Redirect to dashboard based on user role
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect_user_based_on_role(user)  # Redirect based on user role
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def redirect_user_based_on_role(user):
    print(f"Redirecting user: {user.username}, role: {user.role.name}")  # Debugging line
    if user.role.name == 'store_manager':
        return redirect('store_manager_dashboard')
    elif user.role.name == 'inventory_clerk':
        return redirect('inventory_clerk_dashboard')
    elif user.role.name == 'supplier':
        return redirect('supplier_dashboard')
    elif user.role.name == 'system_admin':
        return redirect('system_admin_dashboard')
    return redirect('landing_page')


def user_logout(request):
    auth_logout(request)
    return redirect('landing_page')

def dashboard(request):
    products = Product.objects.all()
    low_stock_alerts = [p for p in products if p.stock < p.reorder_point]
    return render(request, 'dashboard.html', {
        'low_stock_alerts': low_stock_alerts,
        'products': products,
        'orders': Order.objects.all(),
        'suppliers': Supplier.objects.all(),
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

def landing_page(request):
    return render(request, 'landing_page.html')

def product_visualization(request):
    products = Product.objects.all()

    # Bar Chart for Product Stock Levels
    bar_data = {
        'Product': [product.name for product in products],
        'Stock': [product.stock for product in products],
    }
    bar_fig = px.bar(bar_data, x='Product', y='Stock', title="Product Stock Levels")
    bar_chart = plot(bar_fig, output_type='div')

    # Pie Chart for Product Stock Distribution
    pie_data = {
        'Product': [product.name for product in products],
        'Stock': [product.stock for product in products],
    }
    pie_fig = px.pie(pie_data, names='Product', values='Stock', title="Product Stock Distribution")
    pie_chart = plot(pie_fig, output_type='div')

    return render(request, 'product_visualization.html', {
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
    })

# New role-specific dashboard views
@user_passes_test(lambda u: u.role.name == 'inventory_clerk')
def inventory_clerk_dashboard(request):
    return render(request, 'welcome_dashboard.html')

@user_passes_test(lambda u: u.role.name == 'supplier')
def supplier_dashboard(request):
    return render(request, 'supplier_dashboard.html')

@user_passes_test(lambda u: u.role.name == 'system_admin')
def system_admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Dashboard for Store Managers
@user_passes_test(lambda u: u.role.name == 'store_manager')
def store_manager_dashboard(request):
    return render(request, 'dashboard.html')
