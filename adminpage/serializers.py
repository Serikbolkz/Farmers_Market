from rest_framework import serializers
from .models import Buyer,PendingFarmer, Farmer, Farm, Product, Order

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['username', 'password', 'full_name', 'email', 'phone_number', 'address', 'image']
        extra_kwargs = {
            'image': {'required': False}
        }

class PendingFarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingFarmer
        fields = ['username', 'password', 'email', 'name', 'surname', 'phonenumber', 'farm_location', 'image']
        extra_kwargs = {
            'image': {'required': False},
        }

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id', 'name', 'surname', 'farm_location', 'image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'quantity']

class FarmSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Farm
        fields = ['id', 'location', 'farm_name', 'types_of_crops', 'size', 'products']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['buyer', 'farm', 'order_date', 'order_status']

class FarmSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['farmer', 'location', 'farm_name', 'types_of_crops', 'size']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['farm', 'product_name', 'price', 'quantity']