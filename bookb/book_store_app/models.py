from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be a staff'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be a superuser'
            )
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):

    pk_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True,max_length=255,blank=False)
    first_name = models.CharField('first name',max_length=150,blank=True)
    last_name = models.CharField('last name',max_length=150,blank=True)
    mobile= models.PositiveBigIntegerField('mobile',null=True,blank=True)
    is_staff = models.BooleanField('staff status',default=True)
    is_active = models.BooleanField('active',default=True)
    is_superuser = models.BooleanField('superuser',default=False)
    date_joined = models.DateTimeField('date joined',default=timezone.now)
    otp = models.IntegerField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    otp_link = models.TextField(unique=True, blank=True, null=True)
    otp_created_time = models.DateTimeField(blank=True, null=True)
  
    USERNAME_FIELD = 'email'
    objects = UserManager()
    def __str__(self):
        return self.email
    def full_name(self):
        return self.first_name+" "+self.last_name


class UserSiteSettings(models.Model):

    fk_user = models.ForeignKey('User', on_delete=models.DO_NOTHING, db_column='fk_user', db_index=True)
    dark_theme = models.BooleanField(default=False)
    

class UserProperties(models.Model):
    pk_user_property = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('User', on_delete=models.DO_NOTHING, db_column='fk_user', db_index=True)
    fk_user_property_type = models.ForeignKey('UserPropertiesTypes', on_delete=models.DO_NOTHING,
                                              db_column='fk_user_property_type')
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users_properties'


class UserPropertiesTypes(models.Model):
    pk_user_property_type = models.AutoField(primary_key=True)
    key = models.CharField(unique=True, max_length=55)
    description = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        managed = True
        db_table = 'users_properties_types'

class BBRoles(models.Model):
    pk_role = models.AutoField(primary_key=True)
    key = models.CharField(unique=True, max_length=55)
    description = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        managed = True
        db_table = 'roles'


class BBComponents(models.Model):
    pk_component = models.AutoField(primary_key=True)
    key = models.CharField(unique=True, max_length=55)
    description = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        managed = True
        db_table = 'components'


class BBRolesComponents(models.Model):
    pk_role_component = models.AutoField(primary_key=True)
    fk_role = models.ForeignKey('BBRoles', on_delete=models.CASCADE, db_column='fk_role', db_index=True)
    fk_component = models.ForeignKey('BBComponents', on_delete=models.CASCADE, db_column='fk_component')

    class Meta:
        managed = True
        db_table = 'roles_components'
        unique_together = (('fk_role', 'fk_component'),)


class BBUserComponents(models.Model):
    pk_user_component = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='fk_user')
    fk_component = models.ForeignKey('BBComponents', on_delete=models.CASCADE, db_column='fk_component')

    class Meta:
        managed = True
        db_table = 'users_components'
        unique_together = (('fk_user', 'fk_component'),)


class BBUserRoles(models.Model):
    pk_user_role = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='fk_user', db_index=True)
    fk_role = models.ForeignKey('BBRoles', on_delete=models.CASCADE, db_column='fk_role')

    class Meta:
        managed = True
        db_table = 'users_roles'
        unique_together = (('fk_user', 'fk_role'),)



class Books(models.Model):

    pk_book = models.AutoField(primary_key=True)
    title = models.CharField(max_length=55)
    author = models.CharField(max_length=55)
    genre = models.CharField(max_length=55)
    thumbnail = models.FileField(upload_to='media/')
    descriptions = models.TextField(blank=True)
    publisher = models.CharField(max_length=55)
    price = models.FloatField()
    total_stock = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'books'



class UserCart(models.Model):

    pk_cart = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='fk_user')
    fk_book = models.ForeignKey('Books', on_delete=models.CASCADE, db_column='fk_book')
    items = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)

    class Meta:
        managed = True
        db_table = 'usercart'


class UserProduct(models.Model):

    pk_user_product = models.AutoField(primary_key=True)
    fk_user_cart = models.ForeignKey('UserCart', on_delete=models.CASCADE, db_column='fk_user')
    created_at = models.DateTimeField(auto_now=True)
    updated_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'user_product'


class UserNotification(models.Model):

    pk_user_notification = models.AutoField(primary_key=True)
    title =  models.CharField(max_length=55)
    body = models.TextField()

    class Meta:
        managed = True
        db_table = 'user_notification'


class Ticket(models.Model):

    pk_ticket = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='fk_user')
    subject = models.CharField(max_length=55)
    description = models.TextField()
    is_closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'ticket'



class TicketConversation(models.Model):

    pk_ticket_conversation = models.AutoField(primary_key=True)
    fk_ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, db_column='fk_user')
    text = models.TextField()
    name = models.CharField(max_length=55)
    admin_name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now=True)
    updated_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'ticket_conversation'

        