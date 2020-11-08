from django.shortcuts import render
from django.http import HttpResponse
from .models import Items, Purchase, Vendor, PurchaseReturn, Sales, SalesReturn, RetailID
from django.db.models import OuterRef, Subquery
from datetime import date
import datetime

# Create your views here.


def index(request):
    return render(request, 'index.html')


def loginPost(request):
    uname = request.POST['uname']
    pwd = request.POST['pwd']
    error = False
    if((uname != "admin" or pwd != "admin")):
        error = True
    if(error == False):
        return render(request, 'home.html')
    else:
        mydictionary = {
            "error": error,
        }
        return render(request, 'index.html', mydictionary)


def home(request):
    return render(request, 'home.html')


def purchase(request):
    v = Vendor.objects.all()
    mydict = {
        "v": v,
        "submit": False,
        "pur_id": None,
    }
    return render(request, 'purchase.html', context=mydict)


def addExistingPurchase(request):
    p_id = None
    item_id = request.POST.get('item')
    expiry = request.POST['expiry']
    i = Items.objects.get(id=item_id)
    name = i.item_name
    batch = request.POST['batch']
    quantity = request.POST['quantity']
    price = request.POST['price']
    retail_id = batch + '/' + name
    vendor = request.POST.get('vendor')
    v = Vendor.objects.get(id=vendor)
    total = float(quantity) * float(price)
    item_quantity = float(quantity)
    item_price = price
    try:
        new_retail = RetailID(
            item_id=i,
            retail_id=retail_id,
            expiry=expiry,
            item_quantity = item_quantity,
            item_price = item_price
        )
        new_retail.save()
        new_purchase = Purchase(
            item_id=i,
            item_batch=batch,
            item_quantity=quantity,
            item_price=price,
            retail_id = new_retail,
            item_total=total,
            vendor_id=v,
        )
        new_purchase.save()
        p_id = new_purchase.id
        retail_err = False
        submit = True
    except:
        retail_err = True
        submit = False

    i = Items.objects.all()
    v = Vendor.objects.all()
    return render(request, 'purchaseExisting.html', {"pur_id": p_id,"i": i, "v": v, "exist": False, "submit": submit, "retail_err": retail_err})


def existingPurchase(request):
    i = Items.objects.all()
    v = Vendor.objects.all()
    return render(request,  'purchaseExisting.html', {"pur_id": None,"i": i, "v": v, "exist": False, "submit": False})


def addPurchase(request):
    name = request.POST['itemname']
    batch = request.POST['batch']
    quantity = request.POST['quantity']
    price = request.POST['price']
    vendor = request.POST.get('vendor')
    v = Vendor.objects.get(id=vendor)
    expiry = request.POST['expiry']
    total = float(quantity) * float(price)
    i = Items.objects.filter(item_name = name)
    retail_id = batch + '/' + name

    if not i.exists():
        try:
            new_item = Items(
                item_name=name,
            )
            new_item.save()

            new_retail = RetailID(
                item_id = new_item,
                retail_id = retail_id,
                expiry = expiry,
                item_quantity=quantity,
                item_price=price,
            )
            new_retail.save()

            new_purchase = Purchase(
                item_id=new_item,
                item_batch=batch,
                item_quantity=quantity,
                item_price=price,
                item_total=total,
                retail_id = new_retail,
                vendor_id=v,
            )
            new_purchase.save()
            p_id = new_purchase.id
            v = Vendor.objects.all()
            context = {
                "err": False,
                "submit": True,
                "v": v,
                "pur_id": p_id,
            }
        except:
            v = Vendor.objects.all()
            context = {
                "err": True,
                "submit": False,
                "v": v,
                "pur_id":None
            }
        return render(request, 'purchase.html', context)
    else:
        i = Items.objects.all()
        v = Vendor.objects.all()
        return render(request, 'purchaseExisting.html', {"i": i, "v": v, "exist": True, "submit": False})


def returnPurchase(request):
    p = Purchase.objects.all().select_related()
    context = {
        "submit": False,
        "p": p,
        "low_stock": False,
        "high_stock": False,
    }
    return render(request, 'returnPurchase.html', context)


def returnPurchaseAdd(request):
    low_stock = False
    high_stock = False
    submit = False
    pid = request.POST['purchase_id']
    quantity = request.POST['quantity']
    reason = request.POST['reason']
    p = Purchase.objects.get(id=pid)
    retail_id = p.retail_id
    rtotal = float(quantity) * float(p.item_price)
    pquantity = p.item_quantity
    item = p.item_id
    r = RetailID.objects.get(retail_id = retail_id)
    if float(quantity) > float(r.item_quantity):
        low_stock = True
    elif float(quantity) > float(p.item_quantity):
        high_stock = True

    if low_stock == False and high_stock == False:
        pr = PurchaseReturn(
            purchase_id=p,
            return_quantity=float(quantity),
            return_total=rtotal,
            return_reason=reason,
        )
        pr.save()
        r.item_quantity = float(r.item_quantity) - float(quantity)
        r.save()
        submit = True

    p = Purchase.objects.all().select_related()
    context = {
        "low_stock": low_stock,
        "p": p,
        "submit": submit,
        "high_stock": high_stock,
    }
    return render(request, 'returnPurchase.html', context)


def retail(request):
    i = Items.objects.all()
    return render(request, 'retail.html',{"selectedId":None,"selected":False,"i":i,})

def salePostRetailSelect(request):
    item = request.POST.get('item')
    r = RetailID.objects.filter(item_id = item) & RetailID.objects.filter(item_quantity__gt = 0)
    i = Items.objects.all()
    return render(request, 'retail.html',{"selectedId":item,"selected":True,"i":i, "r":r})


def salePost(request):
    i = Items.objects.all()
    r = RetailID.objects.all()
    item_id = request.POST.get('item')
    retail_id = request.POST.get('retailid')
    quantity = request.POST['quantity']
    stockout = False
    success = False
    sale_id = None
    match = True
    try:
        print(retail_id)
        print(item_id)
        check = RetailID.objects.filter(item_id = item_id) & RetailID.objects.filter(id = retail_id)
        print(check)
        if not check:
            match = False
            return render(request,'retail.html',{"selectedId":None,"selected":False,"salesid":sale_id,"match":match,"success":success,"stockout":stockout,"i":i, "r":r})
        else:
            print("else")
            re = RetailID.objects.get(id = retail_id)
            print("else1")
            if float(quantity) > float(re.item_quantity):
                print("if inside else")
                stockout = True
                return render(request, 'retail.html',{"selectedId":None,"selected":False,"salesid":sale_id,"match":match,"success":success,"stockout":stockout,"i":i, "r":r})
            else:
                print("else inside else")
                re.item_quantity = float(re.item_quantity) - float(quantity)
                print("else inside else1")
                total = float(quantity) * float(re.item_price)
                print("else inside else2")
                re.save()
                print("else inside else3")
                itemSelled = Items.objects.get(id = item_id)
                print("else inside else3.5")
                new_sale = Sales(
                    item_id = itemSelled,
                    retail_id = re,
                    sales_quantity = quantity,
                    sales_total = total,
                )
                print("else inside else4")
                new_sale.save()
                print("else inside else5")
                sale_id = new_sale.id
                success = True
    except:
        success = False
        print("except")
    return render(request, 'retail.html',{"selectedId":None,"selected":False,"salesid":sale_id,"match":match, "success":success,"stockout":stockout,"i":i, "r":r})

def returnRetail(request):
    s = Sales.objects.all()
    high_stock = False
    return_period = False
    print(s)
    context = {
        "s" : s,
        "high_stock": high_stock,
        "return_period": return_period,
        "returned":False
    }
    return render(request, 'returnRetail.html', context)


def returnRetailPost(request):
    high_stock = False
    returned = False
    return_period = False
    sid = request.POST['salesid']
    quantity = request.POST['quantity']
    reason = request.POST['reason']
    s = Sales.objects.get(id=sid)
    retail_id = s.retail_id
    r = RetailID.objects.get(retail_id = retail_id)
    rtotal = float(quantity) * float(r.item_price)
    squantity = s.sales_quantity
    item = s.item_id
    sdate = s.sales_date
    tdate = datetime.datetime.now()
    if tdate.day > sdate.day:
        return_period = True
    if float(quantity) > float(s.sales_quantity):
        high_stock = True
    if high_stock == False and return_period == False:
        sr = SalesReturn(
            sales_id=s,
            return_quantity = quantity,
            return_total = rtotal,
            return_reason = reason,
        )
        sr.save()
        r = RetailID.objects.get(retail_id = retail_id)
        r.item_quantity = float(r.item_quantity) + float(quantity) 
        r.save()
        returned = True
    s = Sales.objects.all()
    context = {
        "s" : s,
        "high_stock": high_stock,
        "return_period" : return_period,
        "returned": returned
    }
    return render(request, 'returnRetail.html', context)

def pricing(request):
    items_qs = Items.objects.filter(id = OuterRef("pk")).select_related().order_by("item_name")
    r = RetailID.objects.all().annotate(item_name = Subquery(items_qs.values('item_name')[:1])).select_related()
    context = {
        'i': r
    }
    return render(request, 'pricing.html', context)


def editPrice(request, item_id):
    r = RetailID.objects.filter(id=item_id)
    print(r)
    context = {
        "i": r,
        "submit": False,
    }
    return render(request, 'editPrice.html', context)


def savePrice(request):
    new_price = request.POST['price']
    item_id = request.POST['item_id']
    retail_id = request.POST.get('retail_id')
    r = RetailID.objects.get(retail_id=retail_id)
    r.item_price = new_price
    r.save()
    r = RetailID.objects.filter(item_id=item_id).select_related()
    context = {
        "i": r,
        "submit": True,
    }
    return render(request, 'editPrice.html', context)


def purchasehistory(request):
    p = Purchase.objects.all().select_related().order_by('-purchase_date')
    return render(request, 'purchaseHistory.html',{"p":p})



def purchasereturnhistory(request):
    pr = PurchaseReturn.objects.all().select_related().order_by('-return_date')
    return render(request, 'purchaseReturnHistory.html',{"pr":pr})


def retailhistory(request):
    s = Sales.objects.all().select_related().order_by('-sales_date')
    return render(request, 'retailHistory.html',{"s":s})


def salesreturnhistory(request):
    s = SalesReturn.objects.all().select_related().order_by('-return_date')
    return render(request, 'RetailReturnHistory.html')

def itemQuantity(request):
    i = Items.objects.all()
    item_list = []
    quantity_list = []
    for item in i:
        r = RetailID.objects.filter(item_id = item.id).select_related()
        quantity =0.0
        for retail in r:
            quantity = float(quantity) + float(retail.item_quantity)
        item_list.append(item.item_name)
        quantity_list.append(quantity)
    
    leng = len(item_list)
    context ={
        "item": item_list,
        "quantity": quantity_list,
        "length": leng
    }
    return render(request,'quantity.html',context)

def vendor(request):
    v = Vendor.objects.all()
    return render(request,'vendor.html',{"v":v,})

def vendorAdd(request):
    name = request.POST.get('name')
    print(name)
    location = request.POST.get('location')
    phone = request.POST.get('phone')
    new_vendor = Vendor(
        vendor_name =  name,
        vendor_location = location,
        vendor_contact = phone,
    )
    new_vendor.save()
    v = Vendor.objects.all()
    return render(request,'vendor.html',{"v":v,})