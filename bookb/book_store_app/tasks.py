from bookb.celery import app
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

@app.task
def send_email_create_user(email):

    email_content = render_to_string('../templates/welcome_email.html',{'email':email})


    send_mail("Welcome Aboard !",email_content, settings.EMAIL_HOST_USER, [email], html_message=email_content)

@app.task
def send_email_promotion(subject,recipient_list):

    email_content = render_to_string('../templates/promotion_email.html')


    send_mail(subject,email_content, settings.EMAIL_HOST_USER, recipient_list=recipient_list, html_message=email_content)

@app.task
def send_email_otp(otp,email):

    email_content = render_to_string('../templates/otp_email.html',{'otp':otp})

    send_mail("OTP",email_content, settings.EMAIL_HOST_USER, [email], html_message=email_content)

