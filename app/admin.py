from django.contrib import admin
from . import models
# Register your models here.

class  Customer_data(admin.ModelAdmin):
    list_display = ('id','user','full_name','address','joined_on')


class  Category_data(admin.ModelAdmin):
    list_display = ('id','title','slug')


class  Product_data(admin.ModelAdmin):
    list_display = ('id','title','slug','category','image','marked_price','selling_price','description','warranty','return_policy','view_count')


class  Cart_data(admin.ModelAdmin):
    list_display = ('id','customer','total','created_at')


class  CartProduct_data(admin.ModelAdmin):
    list_display = ('id','cart','product','rate','quantity','subtotal')


class Order_data(admin.ModelAdmin):
    list_display = ('id','cart','ordered_by','shipping_address','mobile','email','subtotal','discount','total','order_status','created_at')

admin.site.register(models.Customer, Customer_data)
admin.site.register(models.Category, Category_data)
admin.site.register(models.Product, Product_data)
admin.site.register(models.Cart, Cart_data)
admin.site.register(models.CartProduct, CartProduct_data)
admin.site.register(models.Order, Order_data)