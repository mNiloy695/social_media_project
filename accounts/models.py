from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class CustomManager(BaseUserManager):
    def create(self,**kwargs):
        email=kwargs.get('email')
        if not email:
            raise ValueError("Email address is required")
        email=self.normalize_email(email)
        password=kwargs.get('password')
        user=self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def  create_superuser(self,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        return self.create(**kwargs)


ROLE_TYPE=(
    ('private_lander','private_lander'),
    ('borrower','borrower'),
)
class CustomUserModel(AbstractBaseUser,PermissionsMixin):
    full_name=models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=11,blank=True,null=True)
    role=models.CharField(choices=ROLE_TYPE,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects=CustomManager()
    USERNAME_FIELD="email"

    def __str__(self):
        return f'{self.id}'
    
class ForgotPasswordModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    is_used=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def is_expire_otp(self):
        return timezone.now() > self.created_at+timedelta(minutes=5)
