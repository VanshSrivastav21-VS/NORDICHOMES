from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product, Category

from .forms import SignUpForm

def frontpage(request):
    products = Product.objects.all()[0:8]
    return render(request, 'core/frontpage.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html')

@ login_required
def myaccount(request):
    return render(request, 'core/myaccount.html')

@ login_required
def edit_myaccount(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('myaccount')
    return render(request, 'core/edit_myaccount.html')

def login_old(request):
    return render(request, 'core/login.html')


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category',  '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')

    if query:
        products = products.filter(name__icontains=query)

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    }

    return render(request, 'core/shop.html', context)

def about(request):
    return render(request, 'core/about.html')