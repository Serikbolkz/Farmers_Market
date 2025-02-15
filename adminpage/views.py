import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Admin, Farmer, Farm, Product, Buyer, PendingFarmer, Order
from django.contrib import messages

from farmers_admin.settings import EMAIL_HOST_USER
from functools import wraps
from django.core.mail import send_mail
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BuyerSerializer
from django.contrib.auth.hashers import check_password
from .serializers import PendingFarmerSerializer, FarmSerializer, FarmerSerializer, OrderSerializer, FarmSerializer2, ProductSerializer

def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_user' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def login(request):
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin_user = Admin.objects.get(username=username, password=password)

            verification_code = f"{random.randint(100000, 999999)}"

            request.session['verification_code'] = verification_code
            request.session['admin_user'] = admin_user.username

            send_mail(
                'Your Verification Code',
                f'Your verification code is: {verification_code}',
                EMAIL_HOST_USER,
                ['serikbol.talgatuly@nu.edu.kz'],
                fail_silently=False,
            )

            return redirect('verify')
        except Admin.DoesNotExist:
            error_message = "Invalid Username or Password!"

    return render(request, "login.html", {"error_message": error_message})

def verify(request):
    error_message = None

    if request.method == "POST":
        input_code = request.POST.get("code")
        stored_code = request.session.get('verification_code')

        if input_code == stored_code:
            return redirect("dashboard")
        else:
            error_message = "Invalid verification code!"

    return render(request, "verify.html", {"error_message": error_message})

def dashboard(request):
    if "admin_user" in request.session:
        return render(request, "dashboard.html")
    else:
        return redirect("login")

def logout(request):
    
    request.session.flush()
    return redirect("login")

def forget_password(request):
    error_message = None
    verification_sent = False

    if request.method == "POST":
        if not request.session.get('verification_sent'):
            username = request.POST.get("username")
            try:
                admin_user = Admin.objects.get(username=username)

                verification_code = f"{random.randint(100000, 999999)}"
                request.session['verification_code'] = verification_code
                request.session['reset_username'] = username

                send_mail(
                    'Password Reset Verification Code',
                    f'Your password reset code is: {verification_code}',
                    EMAIL_HOST_USER,
                    ['serikbol.talgatuly@nu.edu.kz'],
                    fail_silently=False,
                )
                verification_sent = True
                request.session['verification_sent'] = True
            except Admin.DoesNotExist:
                error_message = "Invalid username! Please try again."
        else:
            verification_code = request.POST.get("verification_code")
            new_password = request.POST.get("new_password")

            if verification_code == request.session.get('verification_code'):
                username = request.session.get('reset_username')
                admin_user = Admin.objects.get(username=username)
                admin_user.password = new_password
                admin_user.save()

                request.session.flush()
                return redirect('login')
            else:
                error_message = "Invalid verification code!"

    return render(request, "forget_password.html", {
        "error_message": error_message,
        "verification_sent": request.session.get('verification_sent', False)
    })

def main(request):
    return render(request, "main.html")

@admin_login_required
def show_farmers(request):
    farmers = Farmer.objects.all()
    return render(request, 'farmers.html', {'farmers': farmers})

@admin_login_required
def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    return render(request, 'farmer_detail.html', {'farmer': farmer})

@admin_login_required
def delete_farmer(request, pk):
    if request.method == 'POST':
        farmer = get_object_or_404(Farmer, pk=pk)
        farmer.delete()
        messages.success(request, f"Farmer {farmer.name} {farmer.surname} and their farms have been deleted.")
        return redirect('show_farmers')
    else:
        return redirect('farmer_detail', pk=pk)

@admin_login_required
def delete_farm(request, farm_id):
    if request.method == 'POST':
        farm = get_object_or_404(Farm, pk=farm_id)
        farmer_id = farm.farmer.id
        farm.delete()
        messages.success(request, f"Farm '{farm.farm_name}' has been deleted.")
        return redirect('farmer_detail', pk=farmer_id)
    else:
        return redirect('show_farmers')
    
@admin_login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        farm_id = product.farm.id
        product.delete()
        messages.success(request, f"Product '{product.product_name}' has been deleted.")
        return redirect('farmer_detail', pk=product.farm.farmer.id)
    else:
        return redirect('show_farmers')

@admin_login_required   
def show_buyers(request):
    buyers = Buyer.objects.all()
    return render(request, 'buyers.html', {'buyers': buyers})

@admin_login_required
def buyer_detail(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    return render(request, 'buyer_detail.html', {'buyer': buyer})

@admin_login_required
def delete_buyer(request, pk):
    if request.method == 'POST':
        buyer = get_object_or_404(Buyer, pk=pk)
        buyer.delete()
        messages.success(request, f"Buyer {buyer.fullname} has been deleted.")
        return redirect('show_buyers')
    else:
        return redirect('buyer_detail', pk=pk)

@admin_login_required
def show_pendings(request):
    pending_farmers = PendingFarmer.objects.all()
    return render(request, 'pending_farmers.html', {'pending_farmers': pending_farmers})

class RegisterBuyerView(APIView):
    def post(self, request):
        serializer = BuyerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Buyer registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginBuyerView(APIView):
    def post(self, request):
        print("Received request for /api/login_buyer/")
        username = request.data.get("username")
        password = request.data.get("password")
        print("Received data:", request.data)
        try:
            buyer = Buyer.objects.get(username=username)
            
            if buyer.password == password:
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Buyer.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class RegisterFarmerView(APIView):
    def post(self, request):
        serializer = PendingFarmerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Farmer registration request received"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginFarmerView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            farmer = Farmer.objects.get(username=username, password=password)  # Replace with authentication logic
            return Response(
                {
                    "message": "Login successful",
                    "farmerId": farmer.id
                },
                status=status.HTTP_200_OK,
            )
        except Farmer.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def accept_farmer(request, farmer_id):

    pending_farmer = get_object_or_404(PendingFarmer, id=farmer_id)

    Farmer.objects.create(
        username=pending_farmer.username,
        password=pending_farmer.password,
        email=pending_farmer.email,
        name=pending_farmer.name,
        surname=pending_farmer.surname,
        phonenumber=pending_farmer.phonenumber,
        farm_location=pending_farmer.farm_location,
        image=pending_farmer.image,
    )

    message = request.POST.get('message', '')
    send_mail(
        subject="Registration Accepted",
        message=message,
        from_email='serikboltalgatuly1@gmail.com',
        recipient_list=[pending_farmer.email],
    )

    pending_farmer.delete()

    return redirect('show_pendings')

def reject_farmer(request, farmer_id):

    pending_farmer = get_object_or_404(PendingFarmer, id=farmer_id)

    message = request.POST.get('message', '')
    send_mail(
        subject="Registration Rejected",
        message=message,
        from_email='serikboltalgatuly1@gmail.com',
        recipient_list=[pending_farmer.email],
    )

    pending_farmer.delete()

    return redirect('show_pendings')


class FarmerListView(APIView):
    def get(self, request):
        farmers = Farmer.objects.all()
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FarmerDetailsView(APIView):
    def get(self, request, farmer_id):
        try:
            farms = Farm.objects.filter(farmer_id=farmer_id).prefetch_related('products')
            serializer = FarmSerializer(farms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Farmer.DoesNotExist:
            return Response({"error": "Farmer not found"}, status=status.HTTP_404_NOT_FOUND)
        
class CreateOrderView(APIView):
    def post(self, request):
        buyer_id = request.data.get('buyer_id')
        farm_id = request.data.get('farm_id')
        
        try:
            buyer = Buyer.objects.get(id=buyer_id)
            farm = Farm.objects.get(id=farm_id)

            order = Order.objects.create(
                buyer=buyer,
                farm=farm,
                order_date=date.today(),
                order_status="Pending"
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Buyer.DoesNotExist:
            return Response({"error": "Buyer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Farm.DoesNotExist:
            return Response({"error": "Farm not found"}, status=status.HTTP_404_NOT_FOUND)
    

class CreateFarmView(APIView):
    def post(self, request):
        data = request.data
        farmer_id = data.get('farmerId')
        print("Received farm creation request:", data)
        if not farmer_id:
            return Response({"error": "Farmer ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            farmer = Farmer.objects.get(id=farmer_id)
        except Farmer.DoesNotExist:
            return Response({"error": "Farmer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        farm_data = {
            "farmer": farmer.id,
            "location": data.get("location"),
            "farm_name": data.get("farm_name"),
            "types_of_crops": data.get("types_of_crops"),
            "size": data.get("size"),
        }
        print(farm_data)
        serializer = FarmSerializer2(data=farm_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Farm created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddProductView(APIView):
    def post(self, request):
        data = request.data
        farm_id = data.get('farmId')

        if not farm_id:
            return Response({"error": "Farm ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            farm = Farm.objects.get(id=farm_id)
        except Farm.DoesNotExist:
            return Response({"error": "Farm not found"}, status=status.HTTP_404_NOT_FOUND)

        product_data = {
            "farm": farm.id,
            "product_name": data.get("product_name"),
            "price": data.get("price"),
            "quantity": data.get("quantity"),
        }

        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetFarmsForFarmerView(APIView):
    def get(self, request, farmer_id):
        try:
            farms = Farm.objects.filter(farmer_id=farmer_id)
            farm_data = [{"id": farm.id, "farm_name": farm.farm_name} for farm in farms]
            return Response(farm_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetProductsForFarmerView(APIView):
    def get(self, request, farmer_id):
        try:
            farms = Farm.objects.filter(farmer_id=farmer_id)
            products = Product.objects.filter(farm__in=farms)
            product_data = [
                {
                    "id": product.id,
                    "farm": product.farm.farm_name,
                    "product_name": product.product_name,
                    "price": product.price,
                    "quantity": product.quantity,
                }
                for product in products
            ]
            return Response(product_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

