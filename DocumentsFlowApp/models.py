from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def id(self, obj):
        return obj.id

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):

    def create_user(self, username, password, email, group):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password,
            group=group
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, group):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            group=group
            )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    username = models.CharField(max_length=40, unique=True, primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=2)
    # group = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'group']

    def get_full_name(self):
        return self.USERNAME_FIELD

    def get_short_name(self):
        return self.USERNAME_FIELD

    def __str__(self):
        return self.USERNAME_FIELD

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
