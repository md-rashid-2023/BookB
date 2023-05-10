from django.urls import path
from .views import IndexView, RegisterView, LoginView, user_logout, CartView, TicketView, MyTicketView, delete_cart_item, CheckOut, update_theme , PromotionMail , ForgotPassword
from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('', IndexView.as_view(), name='index' ),
   path('register/',RegisterView.as_view(), name='register'),
   path('login/',LoginView.as_view(), name='login'),
   path('logout/',user_logout, name='logout'),
   path('cart/', CartView.as_view(), name='cart' ),
   path('ticket/',TicketView.as_view(), name='ticket' ),
   path('my-ticket/',MyTicketView.as_view(), name='my-ticket' ),
   path('forgot-password',ForgotPassword.as_view(),name='forgot-password'),
   path('delete-cart/<pk>',delete_cart_item, name='delete-cart-item'),
   path('checkout',CheckOut.as_view(), name="checkout" ),
   path('update-theme',update_theme, name="update_theme" ),
   path('promotion-mail',PromotionMail.as_view(),name='promotion-mail')
]
