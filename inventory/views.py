from django.shortcuts import render, redirect
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Supplier


# Define a view called 'dashboard'
@login_required
def dashboard(request):
    products = Product.objects.all()
    low_stock_alerts = [p for p in products if p.stock < p.reorder_point]
    return render(request, 'dashboard.html', {
        'low_stock_alerts': low_stock_alerts,
        'products': products,
        'orders': Order.objects.all(),
        'suppliers': Supplier.objects.all(),
    })


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})


@login_required
def product_visualization(request):
    products = Product.objects.all()
    product_data = list(products.values('name', 'stock', 'price'))
    df = pd.DataFrame(product_data)

    if not df.empty:
        # Create different charts
        # Bar Chart
        bar_fig = go.Figure([go.Bar(x=df['name'], y=df['stock'], name='Stock Levels')])
        bar_html = pio.to_html(bar_fig, full_html=False)

        # Pie Chart
        pie_fig = go.Figure([go.Pie(labels=df['name'], values=df['stock'], name='Stock Distribution')])
        pie_html = pio.to_html(pie_fig, full_html=False)

        # Line Chart
        line_fig = go.Figure([go.Scatter(x=df['name'], y=df['stock'], mode='lines+markers', name='Stock Trend')])
        line_html = pio.to_html(line_fig, full_html=False)
    else:
        bar_html = '<p>No data available to visualize.</p>'
        pie_html = '<p>No data available to visualize.</p>'
        line_html = '<p>No data available to visualize.</p>'

    return render(request, 'product_visualization.html', {
        'bar_chart': bar_html,
        'pie_chart': pie_html,
        'line_chart': line_html,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after registration
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Log in the user
            return redirect(settings.LOGIN_REDIRECT_URL)  # Redirect to the dashboard
        else:
            print(form.errors)  # Print errors if login fails
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
