from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class HunterManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user

class Hunter(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    is_subscribed = models.BooleanField(default=False)
    was_subscribed = models.BooleanField(default=False)

    stripe_session_id = models.CharField(max_length=255, default=None, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, default=None, null=True, blank=True)

    is_admin = models.BooleanField(default=False)

    objects = HunterManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
