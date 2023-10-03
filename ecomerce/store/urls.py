from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update_item/', views.updateItem, name= 'update_item'),
    path('single_item/<int:pk>', views.singleView, name = 'single_item'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name='register'),
    
    path('login/', views.login_view, name='login'),
]