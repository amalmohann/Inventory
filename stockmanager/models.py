from django.db import models

# Create your models here.
class Items(models.Model):
    item_name = models.CharField(max_length = 200)
    item_quantity = models.IntegerField()
    item_price = models.IntegerField()
    # def __str__(self):
    #     return self.item_name

class Vendor(models.Model):
    vendor_name = models.CharField(max_length = 100)
    vendor_location = models.CharField(max_length = 100)

class Purchase(models.Model):
    item_id = models.ForeignKey(Items, on_delete = models.CASCADE)
    item_batch = models.CharField(max_length = 20)
    item_quantity = models.FloatField()
    item_price = models.FloatField()
    item_total = models.FloatField()
    purchase_date = models.DateTimeField(auto_now_add = True)
    # vendor_id= models.ForeignKey(Vendor, on_delete = models.CASCADE)
    retail_id = models.CharField(max_length = 20)

class PurchaseReturn(models.Model):
    # purchase_id = models.ForeignKey(Purchase, on_delete = models.CASCADE)
    return_quantity = models.FloatField()
    return_total = models.FloatField()
    return_date = models.DateTimeField(auto_now_add = True)
    return_reason = models.CharField(max_length = 200)

class Sales(models.Model):
    # item_id = models.ForeignKey(Items, on_delete = models.CASCADE)   
    retail_id = models.CharField(max_length = 20)
    sales_quantity = models.FloatField()
    sales_date = models.DateTimeField(auto_now_add = True)

class SalesReturn(models.Model):
    # sales_id = models.ForeignKey(Sales, on_delete = models.CASCADE)
    return_quantity = models.FloatField()
    return_total = models.FloatField()
    return_date = models.DateTimeField(auto_now_add = True)
    return_reason = models.CharField(max_length = 200)