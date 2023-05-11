from bookb.celery import app
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

@app.task
def send_email_create_user(email):

    """
    Task for sending a welcome email to a newly created user.

    Args:
        email (str): The email address of the user.
    """

    email_content = render_to_string('../templates/welcome_email.html',{'email':email})


    send_mail("Welcome Aboard !",email_content, settings.EMAIL_HOST_USER, [email], html_message=email_content)

@app.task
def send_email_promotion(subject,recipient_list):

    """
    Task for sending a promotional email to a list of recipients.

    Args:
        subject (str): The subject of the email.
        recipient_list (list): A list of email addresses of the recipients.
    """

    email_content = render_to_string('../templates/promotion_email.html')


    send_mail(subject,email_content, settings.EMAIL_HOST_USER, recipient_list=recipient_list, html_message=email_content)

@app.task
def send_email_otp(otp,email):

    """
    Task for sending an email with an OTP (One-Time Password).

    Args:
        otp (str): The OTP to be sent.
        email (str): The email address of the recipient.
    """

    email_content = render_to_string('../templates/otp_email.html',{'otp':otp})

    send_mail("OTP",email_content, settings.EMAIL_HOST_USER, [email], html_message=email_content)

