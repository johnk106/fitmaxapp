from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'fitmaxapp/index-2.html',{})

def pay(request):
    return render(request,'fitmaxapp/pay.html',{})
