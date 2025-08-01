from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url = "/login/")
def logout_page(request):
    logout(request)
    return redirect('/login')

def login_page(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request , 'Invalid username')
            return redirect('/login')
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request , 'Wrong Password')
            return redirect('/login')
        
        else: 
            login(request , user)
            return redirect('/receipes')

    return render(request , 'login.html')

def register_page(request):
    if request.method=='POST':
        data = request.POST

        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request , 'Username already taken')
            return redirect('/register')

        user = User.objects.filter(email = email)

        if user.exists():
            messages.error(request , 'Email already registered')
            return redirect('/register')

        user = User.objects.create(
            first_name = firstname,
            last_name = lastname,
            username = username,
            email = email
        )

        user.set_password(password)
        user.save()

        messages.success(request , 'Account created successfully')

        return redirect('/login')


    return render(request , 'register.html')

@login_required(login_url = "/login/")
def create_receipe(request):
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        Receipe.objects.create(
            receipe_image = receipe_image,
            receipe_description = receipe_description,
            receipe_name = receipe_name
        )

        return redirect('/receipes')
    
    return render(request , 'create_receipe.html')

@login_required(login_url = "/login/")
def receipes(request):
    
    queryset = Receipe.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(receipe_name__icontains=search)
    
    context = {'receipes': queryset}

    return render(request , 'receipes.html' , context)
    # return HttpResponse('Hii Mitro')

@login_required(login_url = "/login/")
def delete_receipe(request, id):
    try:
        receipe = Receipe.objects.get(id=id)
        receipe.delete()
        return redirect('/receipes')
    except Receipe.DoesNotExist:
        return HttpResponse("Receipe not found", status=404)
    
@login_required(login_url = "/login/")
def update_receipe(request, id):
    try:
        receipe = Receipe.objects.get(id=id)
        if request.method == "POST":
            data = request.POST
            receipe.receipe_name = data.get('receipe_name')
            receipe.receipe_description = data.get('receipe_description')
            if 'receipe_image' in request.FILES:
                receipe.receipe_image = request.FILES['receipe_image']
            receipe.save()
            return redirect('/receipes')
        
        context = {'receipe': receipe}
        return render(request, 'update_receipe.html', context)
    except Receipe.DoesNotExist:
        return HttpResponse("Receipe not found", status=404)