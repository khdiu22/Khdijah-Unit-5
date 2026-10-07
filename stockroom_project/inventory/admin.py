from django.contrib import admin 
from .models import Category, Customer, Order, OrderItem, Product
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)