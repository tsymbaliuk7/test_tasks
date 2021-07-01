# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#
#
# class BlogUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if username is None:
#             raise TypeError('Users must have usernames')
#         if email is None:
#             raise TypeError('Users must have emails')
#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, email, password=None):
#         if password is None:
#             raise TypeError('Superusers must have passwords')
#         user = self.model(username=username, email=email, password=password)
#         user.is_superuser = True
#         user.is_admin = True
#         user.is_staff = True
#         user.is_active = True
#         user.save(using=self._db)
#         return user
#
#
# class BlogUser(AbstractBaseUser):
#     username = models.CharField(db_index=True, max_length=255, unique=True)
#     email = models.EmailField(db_index=True, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#     objects = BlogUserManager()
#
#     def __str__(self):
#         return self.username + ' ' + str(self.is_active) + str(self.is_staff)
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(default='', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
