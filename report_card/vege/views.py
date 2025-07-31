from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *

# Create your views here.

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

def receipes(request):
    
    queryset = Receipe.objects.all()
    context = {'receipes' : queryset}

    return render(request , 'receipes.html' , context)
    # return HttpResponse('Hii Mitro')