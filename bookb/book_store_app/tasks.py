from bookb.celery import app
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

@app.task
def send_email_create_user(email):

    email_content = render_to_string('../templates/welcome_email.html',{'email':email})


    send_mail("Welcome Aboard !",email_content, settings.EMAIL_HOST_USER, [email], html_message=email_content)