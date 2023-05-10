from bookb.celery import app
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
@app.task
def send_email_otp(otp,email):
    """
        param:subject: subject of the mail
        param:html_content: formatted html content
        param:recipients: list of recipients
    """
    email_content = render_to_string('../templates/otp_email.html',{'otp':otp})
    send_mail("OTP",email_content, settings.EMAIL_HOST_USER, [email], html_message=email_content)
