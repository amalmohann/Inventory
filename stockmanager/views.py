from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def purchase(request):
    return render(request,'purchase.html')

def retail(request):
    return render(request,'retail.html')

def returnPurchase(request):
    return render(request,'returnPurchase.html')

def returnRetail(request):
    return render(request,'returnRetail.html')

def pricing(request):
    return render(request,'pricing.html')

def loginPost(request):
    uname = request.POST['uname']
    pwd = request.POST['pwd']
    if(uname == "admin" and pwd == "admin"):
        return render(request,'home.html')
    else:
        return HttpResponse("Invalid Credentials")
