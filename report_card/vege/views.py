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

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(receipe_name__icontains=search)
    
    context = {'receipes': queryset}

    return render(request , 'receipes.html' , context)
    # return HttpResponse('Hii Mitro')

def delete_receipe(request, id):
    try:
        receipe = Receipe.objects.get(id=id)
        receipe.delete()
        return redirect('/receipes')
    except Receipe.DoesNotExist:
        return HttpResponse("Receipe not found", status=404)
    
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