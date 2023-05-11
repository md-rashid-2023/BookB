from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from book_store_app.models import User
from book_store_app.tasks import send_email_create_user

@receiver([post_save],sender=User)
def notify_user(sender,created,instance,*args, **kwargs):
    if created:
        send_email_create_user.delay(instance.email)