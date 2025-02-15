from django.db import models
import uuid
from django.utils.timezone import now
from datetime import timedelta
import os
from django.utils.deconstruct import deconstructible

@deconstructible
class RenameFile:
    def __call__(self, instance, filename):
        return f"static/images/{filename}"

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + timedelta(minutes=10)
    

class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)

    def check_credentials(self, username, password):
        return self.username == username and self.password == password
    

class Farmer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default= "example@mail.com")
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    farm_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to=RenameFile(), default='static/images/nopicture.png')

    def __str__(self):
        return f"{self.name} {self.surname}"

class Farm(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    location = models.CharField(max_length=100)  
    farm_name = models.CharField(max_length=20)
    types_of_crops = models.CharField(max_length=150)
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.farm_name

class Product(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product_name} ({self.farm.farm_name})"

class Buyer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='static/images/', default='static/images/nopicture.png', blank=True)
    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField()
    order_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} - {self.order_status}"
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment {self.id} - {self.payment_method} - ${self.amount}"
    
class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='deliveries')
    delivery_address = models.CharField(max_length=100)
    delivery_date = models.DateField()
    delivery_status = models.CharField(max_length=100)

    def __str__(self):
        return f"Delivery {self.id} - {self.delivery_status}"

class PendingFarmer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    farm_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/', default='static/images/nopicture.png')
    email = models.CharField(max_length=50, default= "example@mail.com")
    def __str__(self):
        return f"{self.name} {self.surname}"