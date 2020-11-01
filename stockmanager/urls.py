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
]