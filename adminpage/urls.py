from django.urls import path
from . import views
from .views import RegisterBuyerView, LoginBuyerView, RegisterFarmerView, LoginFarmerView
from .views import FarmerListView, FarmerDetailsView, CreateOrderView, CreateFarmView, AddProductView, GetFarmsForFarmerView,GetProductsForFarmerView

urlpatterns = [
    path("login/", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('verify/', views.verify, name='verify'),
    path("forget_password/", views.forget_password, name="forget_password"),
    path("", views.main, name="main"),

    path('farmers/', views.show_farmers, name='show_farmers'),
    path('farmers/<int:pk>/', views.farmer_detail, name='farmer_detail'),
    path('farmers/<int:pk>/delete/', views.delete_farmer, name='delete_farmer'),
    path('farms/<int:farm_id>/delete/', views.delete_farm, name='delete_farm'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    path('buyers/', views.show_buyers, name='show_buyers'),
    path('buyers/<int:pk>/', views.buyer_detail, name='buyer_detail'),
    path('buyers/<int:pk>/delete/', views.delete_buyer, name='delete_buyer'),

    path('pending_farmers/', views.show_pendings, name='show_pendings'),

    path('api/register_buyer/', RegisterBuyerView.as_view(), name='register_buyer'),
    path('api/login_buyer/', LoginBuyerView.as_view(), name='login_buyer'),
    path('api/register_farmer/', RegisterFarmerView.as_view(), name='register_farmer'),
    path('api/login_farmer/', LoginFarmerView.as_view(), name='login_farmer'),
    path('accept-farmer/<int:farmer_id>/', views.accept_farmer, name='accept_farmer'),
    path('reject-farmer/<int:farmer_id>/', views.reject_farmer, name='reject_farmer'),
    path('api/farmers/', FarmerListView.as_view(), name='farmers'),
    path('api/farmer/<int:farmer_id>/', FarmerDetailsView.as_view(), name='farmer_details'),
    path('api/orders/', CreateOrderView.as_view(), name='create_order'),
    path('api/create_farm/', CreateFarmView.as_view(), name='create_farm'),
    path('create_farm/', CreateFarmView.as_view(), name='create_farm'),

    path('api/add_product/', AddProductView.as_view(), name='add_product'),
    path('api/farms/<int:farmer_id>/', GetFarmsForFarmerView.as_view(), name='get_farms_for_farmer'),
    path('api/farmer/<int:farmer_id>/products/', GetProductsForFarmerView.as_view(), name='get_products_for_farmer'),
]