from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
# Create your models here.


class UserProfileManager(BaseUserManager):
    """ MANAGER PARA PERFILES DE USUARIOS"""
    def _create_user(self,email,name,password, is_staff,is_superuser, **extra_fields):
        ''' Nuevo usuario '''
        if not email:
            raise ValueError("Usuario debe tener un email")
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            name=name,
            is_staff=self.is_staff,
            is_active = True,
            is_superuser=self.is_superuser,
            updated_at=now
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get_by_natural_key(self,username):
        return self.get(**{'{}__iexact'.format(self.model.USERNAME_FIELD):username})
    
    def create_user(self,name,email,password,**extra_fields):
        return self._create_user(email,name,password,False,False,**extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        return self._create_user(email,name,password,True,True,**extra_fields)

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """MODELO BASE PARA USUARIOS"""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        '''Obtener nombre completo del usuario'''
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
