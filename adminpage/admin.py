from django.contrib import admin
from .models import Admin, Farmer, Farm, Product, Buyer, Order, Payment, Delivery, PendingFarmer

admin.site.register(Admin)
admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(Product)
admin.site.register(Buyer)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Delivery)
admin.site.register(PendingFarmer)
