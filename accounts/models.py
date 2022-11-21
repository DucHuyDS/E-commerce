from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class ManagerAccount(BaseUserManager):
    def create_user(self,email,username,first_name,last_name,password=None):
        if not email:
            raise ValueError('Account must have an email')
        if not username:
            raise ValueError('Account must have an username')
        user=self.model(
            email= self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, username,first_name,last_name, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_seller=True
        user.save()
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    notification=models.IntegerField(default=0)
    is_admin=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_seller=models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']

    objects = ManagerAccount()

    def full_name(self):
        return self.last_name+' '+self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class AccountProfile(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='account/profile_picture',blank=True)
    address=models.CharField(max_length=200,blank=True)
    birthday=models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.user.full_name