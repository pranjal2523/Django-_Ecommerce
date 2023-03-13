from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class MyUsermanager(BaseUserManager):

    def _create_user(self, email, password, **xtrafields):
        if not email:
            raise ValueError('enter valid email')
        email = self.normalize_email(email)
        user = self.model(email=email, **xtrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **xtrafields):
        xtrafields.setdefault('is_staff', True)
        xtrafields.setdefault('is_superuser', True)
        xtrafields.setdefault('is_active', True)
        if xtrafields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff = true')
        if xtrafields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser = true')
        return self._create_user(email, password, **xtrafields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(gettext_lazy('staff status'), default=False,
                                   help_text=gettext_lazy('designated whether the user can log in the site'))
    is_active = models.BooleanField(gettext_lazy('active'), default=True,
                                    help_text=gettext_lazy('designated whether this user should be treated as active'))
    USERNAME_FIELD = 'email'
    objects = MyUsermanager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_last_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    address_1 = models.TextField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile"

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]
        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == "":
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()