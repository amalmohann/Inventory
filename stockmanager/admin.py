from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Items)
admin.site.register(Vendor)
admin.site.register(Purchase)
admin.site.register(PurchaseReturn)
admin.site.register(Sales)
admin.site.register(SalesReturn)
admin.site.register(RetailID)