from django.urls import path
from .views import IndexView, RegisterView, LoginView, user_logout, CartView, TicketView, MyTicketView, delete_cart_item, CheckOut
from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('', IndexView.as_view(), name='index' ),
   path('register/',RegisterView.as_view(), name='register'),
   path('login/',LoginView.as_view(), name='login'),
   path('logout/',user_logout, name='logout'),
   path('cart/', CartView.as_view(), name='cart' ),
   path('ticket/',TicketView.as_view(), name='ticket' ),
   path('my-ticket/',MyTicketView.as_view(), name='my-ticket' ),
   path('delete-cart/<pk>',delete_cart_item, name='delete-cart-item'),
   path('checkout',CheckOut.as_view(), name="checkout" )
] 
