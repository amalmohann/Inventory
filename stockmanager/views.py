from django.shortcuts import render
from django.http import HttpResponse
from .models import Items, Purchase, Vendor, PurchaseReturn, Sales, SalesReturn, RetailID
from django.db.models import OuterRef, Subquery

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
        "submit": False
    }
    return render(request, 'purchase.html', context=mydict)


def addExistingPurchase(request):
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
        retail_err = False
        submit = True
    except:
        retail_err = True
        submit = False

    i = Items.objects.all()
    v = Vendor.objects.all()
    return render(request, 'purchaseExisting.html', {"i": i, "v": v, "exist": False, "submit": submit, "retail_err": retail_err})


def existingPurchase(request):
    i = Items.objects.all()
    v = Vendor.objects.all()
    return render(request,  'purchaseExisting.html', {"i": i, "v": v, "exist": False, "submit": False})


def addPurchase(request):
    name = request.POST['itemname']
    batch = request.POST['batch']
    quantity = request.POST['quantity']
    price = request.POST['price']
    vendor = request.POST.get('vendor')
    v = Vendor.objects.get(id=vendor)
    expiry = request.POST['expiry']
    total = int(quantity) * int(price)
    i = Items.objects.filter(item_name = name)
    retail_id = batch + '/' + name
    print("\n")
    print(i)
    print("\n")
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
            v = Vendor.objects.all()
            context = {
                "err": False,
                "submit": True,
                "v": v,
            }
        except:
            v = Vendor.objects.all()
            context = {
                "err": True,
                "submit": False,
                "v": v,
            }
        return render(request, 'purchase.html', context)
    else:
        i = Items.objects.all()
        v = Vendor.objects.all()
        return render(request, 'purchaseExisting.html', {"i": i, "v": v, "exist": True, "submit": False})


def retail(request):
    i = Items.objects.all()
    r = RetailID.objects.all()
    return render(request, 'retail.html',{"i":i, "r":r})

def salePost(request):
    print("SALESPOST")
    i = Items.objects.all()
    r = RetailID.objects.all()
    item_id = request.POST.get('item')
    print(item_id)
    retail_id = request.POST.get('retailid')
    print(retail_id)
    quantity = request.POST['quantity']
    print(quantity)
    stockout = False
    success = False
    sale_id = None
    retail = RetailID.objects.all()
    print(retail)
    try:
        retail = RetailID.objects.filter(id = retail_id)
        print(retail)
        for ret in retail:
            re = RetailID.objects.get(id = ret)
            print(re)
        print(re)
        if float(quantity) > float(re.item_quantity):
            stockout = True
            print("IF CONDITION")
            return render(request, 'retail.html',{"success":success,"stockout":stockout,"i":i, "r":r})
        else:
            print("ELSE CONDITION")
            re.item_quantity = re.item_quantity - float(quantity)
            total = quantity * re.item_price
            re.save()
            new_sale = Sales(
                item_id = item_id,
                retail_id = retail_id,
                sales_quantity = quantity,
                sales_total = total,
            )
            new_sale.save()
            sale_id = new_sale.id
            success = True
    except:
        print("EXCEPT CONDITION")
        success = False

    return render(request, 'retail.html',{"salesid":sale_id, "success":success,"stockout":stockout,"i":i, "r":r})


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
    pid = request.POST['purchase_id']
    quantity = request.POST['quantity']
    reason = request.POST['reason']
    p = Purchase.objects.get(id=pid)
    retail_id = p.retail_id
    rtotal = float(quantity) * float(p.item_price)
    pquantity = p.item_quantity
    item = p.item_id
    r = RetailID.objects.get(retail_id = retail_id)
    if quantity > i.item_quantity:
        low_stock = True

    if quantity > p.item_quantity:
        high_stock = True

    if low_stock == False and high_stock == False:
        pr = PurchaseReturn(
            purchase_id=pid,
            return_quantity=quantity,
            return_total=rtotal,
            return_reason=reason,
        )
        pr.save()

    context = {
        "low_stock": low_stock,
        "high_stock": high_stock,
    }
    return render(request, 'returnPurchase.html', context)

def returnRetail(request):
    s = Sales.objects.all()
    high_stock = False
    return_period = False
    context = {
        "s" : s,
        "high_stock": high_stock,
        "return_period": return_period,
    }
    return render(request, 'returnRetail.html', context)


def returnRetailPost(request):
    high_stock = False
    return_period = False
    rid = request.POST['retail_id']
    quantity = request.POST['quantity']
    reason = request.POST['reason']
    p = Purchase.objects.filter(id=pid)
    rtotal = quantity * p.item_price
    pquantity = p.item_quantity
    item = p.item_id
    i = Items.objects.filter(id=item)
    if quantity > i.item_quantity:
        low_stock = True

    if quantity > p.item_quantity:
        high_stock = True

    if low_stock == False and high_stock == False:
        pr = PurchaseReturn(
            purchase_id=p,
            return_quantity=quantity,
            return_total=rtotal,
            return_reason=reason,
        )
        pr.save()

    context = {
        "high_stock": high_stock,
    }

    return render(request, 'returnRetail.html', context)


def pricing(request):
    items_qs = Items.objects.filter(id = OuterRef("pk"))
    r = RetailID.objects.all().annotate(item_name = Subquery(items_qs.values('item_name')[:1]))
    context = {
        'i': r
    }
    return render(request, 'pricing.html', context)


def editPrice(request, item_id):
    r = RetailID.objects.filter(item_id=item_id).select_related() 
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
    p = Purchase.objects.all().select_related()
    return render(request, 'purchaseHistory.html',{"p":p})



def purchasereturnhistory(request):
    pr = PurchaseReturn.objects.all().select_related()
    return render(request, 'purchaseReturnHistory.html',{"pr":pr})


def retailhistory(request):
    s = SalesReturn.objects.all().select_related()
    return render(request, 'retailHistory.html',{"s":s})


def salesreturnhistory(request):
    return render(request, 'RetailReturnHistory.html')
