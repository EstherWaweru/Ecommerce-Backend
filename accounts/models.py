from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your user account models here


class UserManager(BaseUserManager):
    '''
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    '''
    def _create_user(self,email,password,is_staff,is_superuser,**extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have a an email adress.Please set a proper email address!")

        email=self.normalize_email(email)
        now=timezone.now
        user=self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            last_login=now,
            date_joined=now,
            **extra_fields

        )
        user.set_password(password)
        #use default database as defined in the settings file
        user.save(using=self._db)
        return user
    def create_user(self,email,password,**extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)
        
    def create_superuser(self,email,password,**extra_fields):
        return self._create_user(email,password,True,True,**extra_fields)



    

class User(AbstractBaseUser,PermissionsMixin):
    '''
    Custom user with its custom methods
    '''
    email=models.EmailField(verbose_name="email" ,max_length=254,unique=True)
    first_name=models.CharField(verbose_name="first_name",max_length=254,blank=True)
    last_name=models.CharField(max_length=254,blank=True)
    date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_staff=models.BooleanField(default=False,help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active=models.BooleanField(default=True,help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_superuser=models.BooleanField(default=False,help_text=_('Designates whether the user can log into this admin '
                    'site.Also the user has all the permissions by default. '))
    
    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    #giving verbose names
    class Meta:
        verbose_name_plural="users"
        verbose_name="user"
    def get_full_name(self):
        """
         Returns the first_name_last_name
         """
        full_name= '{} {}'.format(self.first_name,self.last_name)
        return full_name
    def get_short_name(self):
        """
        Returns short name of the user
        """
        return self.first_name
    def __str__(self):
        return self.email
    



