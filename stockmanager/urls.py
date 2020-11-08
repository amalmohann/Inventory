from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('home',views.home,name="home"),
    path('purchase', views.purchase, name="purchase"),
    path('pricing', views.pricing, name="pricing"),
    path('retail', views.retail, name="retail"),
    path('returnPurchase', views.returnPurchase, name="returnPurchase"),
    path('returnRetail', views.returnRetail, name="returnRetail"),
    path('loginPost',views.loginPost,name="loginPost"),
    path('purchasehistory',views.purchasehistory,name="purchasehistory"),
    path('saleshistory',views.retailhistory,name="saleshistory"),
    path('salesreturnhistory', views.salesreturnhistory,name="salesreturnhistory"),
    path('purchasereturnhistory',views.purchasereturnhistory,name="purchasereturnhistory"),
    path('addPurchase', views.addPurchase, name="addPurchase"),
    path('returnPurchaseAdd',views.returnPurchaseAdd,name="returnPurchaseAdd"),
    path('returnRetailPost',views.returnRetailPost,name="returnRetailPost"),
    path('editPrice/<int:item_id>',views.editPrice,name="editPrice"),
    path('savePrice',views.savePrice,name="savePrice"),
    path('existingPurchase',views.existingPurchase,name="existingPurchase"),   
    path('addExistingPurchase',views.addExistingPurchase,name="addExistingPurchase"),
    path('salePost',views.salePost,name="salePost"),
    path('salePostRetailSelect',views.salePostRetailSelect,name="salePostRetailSelect"),
    path('itemQuantity',views.itemQuantity,name="itemQuantity"),
    path('vendor',views.vendor,name="vendor"),
    path('vendorAdd',views.vendorAdd,name="vendorAdd"),
    ]