from django.contrib.auth import models as auth_models
from django.db import models
from django.urls import reverse
from ExpenseTracker.auth_app.managers import AppUserManager


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = 'email'

    objects = AppUserManager()


class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.email}'

    def get_absolute_url(self):
        return reverse('profile detail', kwargs={'pk': self.pk})