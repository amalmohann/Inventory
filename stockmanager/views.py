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
    error = False
    if((uname != "admin" or pwd != "admin")):
        error = True
    if(error == False):
        return render(request,'home.html')
    else:
        mydictionary={
            "error" : error,
        }
        return render(request,'index.html',mydictionary)
        
def purchasehistory(request):
    return render(request,'purchaseHistory.html')

def purchasereturnhistory(request):
    return render(request,'purchaseReturnHistory.html')