from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from book_store_app.tasks import send_email_otp
from book_store_app.models import User, Books, UserCart, UserSiteSettings, Ticket, TicketConversation
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import  check_password
from django.db.models import Q
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from book_store_app.tasks import send_email_promotion
import json
import random


def user_logout(request):
    """
    Logs out the user and redirects to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the login page.
    """

    logout(request)

    return redirect('login')


def get_cart_count(request):

    """
    Calculates the total count of items in the user's cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        int: The total count of items in the user's cart.
    """

    total = 0
    if  request.user.is_authenticated:
        total_cart = UserCart.objects.filter(fk_user=request.user)
        total_cart = total_cart.annotate(total_count=Sum("items")).values()


        for item in total_cart:
            total += item['items']

    return total


class IndexView(View):

    """
    View for the index page.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the index page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template with books, search query, and cart count.
        """

        q = request.GET.get('q','')

        if q:
            books = Books.objects.filter(Q(title__icontains=q)|Q(author__icontains=q)|Q(genre__icontains=q))
        else:
            books = Books.objects.all()


        return render(request, self.template_name, { 'books' : books , 'q' :q ,'cart_count' : get_cart_count(request)})



def delete_cart_item(request, pk):

    """
    Deletes a cart item identified by the given primary key.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the cart item to be deleted.

    Returns:
        HttpResponseRedirect: A redirect response to the cart page.
    """

    cart = UserCart.objects.get(pk_cart=pk)
    cart.delete()
    return redirect('cart')


def update_theme(request):

    """
    Updates the user's site theme preference.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the index page.
    """

    try:
        theme = UserSiteSettings.objects.get(fk_user=request.user)
        theme.dark_theme =  not theme.dark_theme
        theme.save()
        request.session["dark_theme"]  = theme.dark_theme
    except Exception as e:
        UserSiteSettings.objects.create(fk_user=request.user, dark_theme=True)
        request.session["dark_theme"] = True

    return redirect('index')


class CartView(View):

    """
    View for the cart page.

    Attributes:
        login_url (str): The URL to redirect to if the user is not authenticated.
        template_name (str): The name of the template to be rendered.
    """

    login_url="login"

    template_name = 'cart.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Custom dispatch method that checks if the user is authenticated before processing the request.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: A redirect response to the login page if the user is not authenticated.
        """

        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super(CartView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the cart page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template with cart information.
        """

        carts_lists = UserCart.objects.filter(fk_user=request.user)

        return render(request, self.template_name, {'cart_count' : get_cart_count(request), 'cart_lists' : carts_lists })

    def post(self, request, *args, **kwargs):

        """
        Handles POST requests for adding items to the cart.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: The JSON response object containing the success message and total cart count.
        """

        pk_book = json.load(request)['pk_book']

        book = Books.objects.get(pk_book=pk_book)

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

        return JsonResponse({'message' : 'success', 'total_cart' : get_cart_count(request)})




class RegisterView(View):

    """
    View for user registration.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the registration page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        """
        Handles POST requests for user registration.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template with the registration status message.
        """

        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user( email=email,
                                    password=password)
            user.username = email
            user.save()
            UserSiteSettings.objects.create(fk_user=user)

            return render(request, self.template_name,   { 'message' : 'Account Successfully Created' } )
        except Exception as e:
            print(' i am here', e)
            return render(request, self.template_name,  { 'message' : 'Account Creation Failed {}'.format(e) })


class TicketView(View):

    """
    View for creating and displaying tickets.

    Attributes:
        template_name (str): The name of the template to be rendered.
        login_url (str): The URL to redirect to if the user is not authenticated.
    """

    template_name = 'ticket.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):

        """
        Custom dispatch method that checks if the user is authenticated before processing the request.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: A redirect response to the login page if the user is not authenticated.
        """

        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super(TicketView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the ticket page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        """
        Handles POST requests for creating tickets.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: A redirect response to the ticket page.
        """

        name = request.POST.get('name')
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        ticket = Ticket.objects.create(
            fk_user = request.user ,
            subject = subject, 
            description = content
        )

        TicketConversation.objects.create(
            fk_ticket = ticket, 
            text = content,
            name = name, 
            admin_name = 'BookB Admin',
        )

        return redirect('ticket')



class CheckOut(View):

    """
    View for the checkout page.

    Attributes:
        template_name (str): The name of the template to be rendered.
        login_url (str): The URL to redirect to if the user is not authenticated.
    """

    template_name = 'sample_checkout.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):

        """
        Custom dispatch method that checks if the user is authenticated before processing the request.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: A redirect response to the login page if the user is not authenticated.
        """

        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super(CheckOut, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the checkout page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """

        return render(request, self.template_name)




class MyTicketView(View):

    """
    View for displaying user's tickets.

    Attributes:
        template_name (str): The name of the template to be rendered.
        login_url (str): The URL to redirect to if the user is not authenticated.
    """

    template_name = 'my-ticket.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Custom dispatch method that checks if the user is authenticated before processing the request.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponseRedirect: A redirect response to the login page if the user is not authenticated.
        """
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super(MyTicketView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the user's ticket page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template with the user's tickets.
        """

        tickets = TicketConversation.objects.filter(fk_ticket__fk_user=request.user).order_by('-updated_at')

        return render(request, self.template_name, { 'tickets' : tickets })

    def post(self, request, *args, **kwargs):

        pass

class LoginView(View):

    """
    View for user login.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):

        """
        Handles GET requests for the login page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """

        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):

        """
        Handles POST requests for user login.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template with the login status message.
        """

        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            is_valid = check_password(password, user.password)
            if is_valid:
                login(request, user)

                if UserSiteSettings.objects.filter(fk_user=user).exists():
                    request.session["dark_theme"] = UserSiteSettings.objects.get(fk_user=user).dark_theme

                return redirect('index')

        except Exception as e:
            print(e)

        return render(request, self.template_name, { 'message' : 'login faild, please check email/password' })

class PromotionMail(View):

    """
    View for sending promotion emails.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """
    
    template_name = 'promotion.html'

    def get(self,request,*args, **kwargs):

        """
        Handles GET requests for the promotion page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template with the list of users.
        """
       
        context = {}
        context['users'] = User.objects.all()
        if request.user.is_superuser:
            return render(request,self.template_name,context=context)
        else:
            return redirect('index')

    def post(self,request,*args, **kwargs):

        """
        Handles POST requests for sending promotion emails.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: A JSON response containing the list of selected users for promotion email.
        """
        

        action = request.POST.get('action','')
        if action == 'send_mass_mail':
            users = request.POST.getlist('users[]','')
            subject = request.POST.get('subject','Promotion Mail')
            print(users)
            if 'all' in users:
                receiver_list = list(User.objects.all().values_list('email',flat=True))
                send_email_promotion.delay(subject,receiver_list)
                return JsonResponse({'data':users})
            else:
                receiver_list = list(User.objects.filter(email__in=users).values_list('email',flat=True))
                send_email_promotion.delay(subject,receiver_list)
                return JsonResponse({'data':users})
        else:
            return redirect('index')
        

class ForgotPassword(View):

    """
    View for handling forgot password functionality.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = 'forgot-password.html'

    def get(self,request,*args, **kwargs):

        """
        Handles GET requests for the forgot password page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """

        return render(request,self.template_name)

    def post(self,request,*args, **kwargs):

        """
        Handles POST requests for the forgot password functionality.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse or HttpResponse: A JSON response or redirect response based on the action performed.
        """

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

class Admin(View):

    """
    View for the admin panel.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = 'admin.html'

    def get(self,request,*args, **kwargs):

        """
        Handles GET requests for the admin panel.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object containing the rendered template.
        """

        return render(request,self.template_name)