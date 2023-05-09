from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from book_store_app.tasks import send_email_otp
from book_store_app.models import User, Books, UserCart
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import  check_password
from django.db.models import Q
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
import json
import random
# Create your views here.


# def index(request):

#     send_email.delay()
#     print('testing celery')

#     return render(request, 'index.html')

def user_logout(request):

    logout(request)

    return redirect('login')


class IndexView(View):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        q = request.GET.get('q','')

        if q:
            books = Books.objects.filter(Q(title__icontains=q)|Q(author__icontains=q)|Q(genre__icontains=q))
        else:
            books = Books.objects.all()

        total = 0
        if  request.user.is_authenticated:
            total_cart = UserCart.objects.filter(fk_user=request.user)
            total_cart = total_cart.annotate(total_count=Sum("items")).values()


            for item in total_cart:
                total += item['items']

        return render(request, self.template_name, { 'books' : books , 'q' :q ,'cart_count' : total})



class CartView(View, LoginRequiredMixin):

    login_url="login"

    template_name = 'cart.html'

    def post(self, request, *args, **kwargs):

        pk_book = json.load(request)['pk_book']

        book = Books.objects.get(pk_book=pk_book)
        total_cart = 0

        if UserCart.objects.filter(fk_user=request.user, fk_book_id=pk_book).exists():

            cart_items = UserCart.objects.filter(fk_user=request.user, fk_book_id=pk_book).last()
            cart_items.items += 1
            cart_items.total_price += cart_items.total_price
            cart_items.save()

        else:
            UserCart.objects.create(
                fk_user=request.user,
                fk_book=book,
                items=1,
                total_price=book.price
            )

        total_cart = UserCart.objects.filter(fk_user=request.user)
        total_cart = total_cart.annotate(total_count=Sum("items")).values()

        total = 0
        for item in total_cart:
            total += item['items']


        return JsonResponse({'message' : 'success', 'total_cart' : total})



class RegisterView(View):

    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user( email=email,
                                    password=password)
            user.username = email
            user.save()
            print('here')
            return render(request, self.template_name,   { 'message' : 'Account Successfully Created' } )
        except Exception as e:
            print(' i am here')
            return render(request, self.template_name,  { 'message' : 'Account Creation Failed {}'.format(e) })


class TicketView(View):

    template_name = 'ticket.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        pass


class MyTicketView(View):

    template_name = 'my-ticket.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        pass




class LoginView(View):

    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):

        email = request.POST.get('email')
        password = request.POST.get('password')

        print('Values: ',email, password)
        user = User.objects.get(email=email)
        is_valid = check_password(password, user.password)

        if is_valid:

            login(request, user)
            print('valid user')
            return redirect('index')

        return render(request, self.template_name, { 'message' : 'login faild, please check email/password {}'.format(user)  })


class ForgotPassword(View):

    template_name = 'forgot-password.html'

    def get(self,request,*args, **kwargs):

        return render(request,self.template_name)

    def post(self,request,*args, **kwargs):

        action = request.POST.get('action','')

        if action  == 'forgot-password':
            message = ''
            email = request.POST.get('email','')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                otp = random.randint(100000, 999999)
                user.otp = otp
                user.save()
                send_email_otp.delay(otp,email)
                message = 'OTP sent to given mail id'

            else:
                message = 'User does not exist'

            return JsonResponse({'data': message})

        if action  == 'verify-otp':
            message = ''
            is_verified = False
            otp = request.POST.get('otp','')
            email = request.POST.get('email','')
            if User.objects.filter(email=email,otp=otp).exists():
                user = User.objects.get(email=email)
                user.otp_verified = True
                user.save()
                message = 'OTP Verified'
                is_verified = True
            else:
                message = 'OTP Not Verified'

            return JsonResponse({'data': message,'is_verified':is_verified})

        if action == 'update-password':
            password = request.POST.get('password','')
            email = request.POST.get('email','')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.password = make_password(password=password)
                user.save()
                return redirect('login')
            return JsonResponse({'data':'User Does not Exist'})
        return render(request,self.template_name)

class ChangePassword(View):

    template_name = 'change-password.html'

    def get(self,request,*args, **kwargs):
        return render(request,self.template_name)

    def post(self,request,*args, **kwargs):
        pass