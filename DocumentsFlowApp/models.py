import datetime

import django
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from decimal import Decimal
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True)
    superior = models.IntegerField(null=True, default=-1)

    def get_superior(self):
        return self.superior

    def id(self, obj):
        return obj.id

    def get_name(self):
        return self.name

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
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def id(self, obj):
        return obj.id


class Flux(models.Model):
    documents = models.CharField(max_length=40, unique=False)
    name = models.CharField(max_length=256, null=True, unique=True)

    def id(self, obj):
        return obj.id

    def get_documents(self):
        return self.documents

    def set_documents(self, documents):
        self.documents = documents

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


class Assigment(models.Model):
    documentTypes = models.CharField(max_length=40, unique=False)
    board = models.IntegerField(default=-1)
    flux = models.ForeignKey(Flux, on_delete=models.CASCADE, default=2)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=2)
    days = models.IntegerField(default=-1)
    step = models.IntegerField(default=-1)

    def id(self, obj):
        return obj.id

    def get_days(self):
        return self.days

    def get_step(self):
        return self.step

    def get_document_types(self):
        return self.documentTypes

    def get_board(self):
        return self.board

    def get_flux(self):
        return self.flux

    def get_user(self):
        return self.user

    def set_document_types(self, documentTypes):
        self.documentTypes = documentTypes

    def set_board(self, board):
        self.board = board

    def set_flux(self, flux_id):
        self.flux = flux_id

    def set_user(self, user_id):
        self.user = user_id

    def set_days(self, days):
        self.days = days

    def set_step(self, step):
        self.step = step



class Template(models.Model):
    keys = models.CharField(max_length=256, unique=False)
    name = models.CharField(max_length=256, null=True, unique=True)

    def id(self, obj):
        return obj.id

    def get_keys(self):
        return self.keys

    def get_name(self):
        return self.name

    def set_keys(self, keys):
        self.keys = keys

    def set_name(self, name):
        self.name = name


class Process(models.Model):
    starter = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=2)
    flux = models.ForeignKey(Flux, on_delete=models.CASCADE, default=2)
    status = models.CharField(max_length=40, unique=False, default="inactiv")

    def id(self, obj):
        return obj.id

    def get_flux(self):
        return self.flux

    def get_status(self):
        return self.status

    def set_status(self,status):
        self.status = status

    def get_starter(self):
        return self.starter

    def set_flux(self, flux_id):
        self.flux = flux_id

    def set_starter(self, user_id):
        self.starter = user_id


class Task(models.Model):
    process = models.ForeignKey(Process, default=2)
    assigment = models.ForeignKey(Assigment, on_delete=models.CASCADE, default=2, null=True)
    deadline = models.DateField(auto_now=False)
    status = models.CharField(max_length=40, unique=False)
    step = models.IntegerField(default = -1)


    def get_step(self):
        return self.step;
    def set_step(self, step):
        self.step =step

    def get_process(self):
        return self.process

    def get_assigment(self):
        return self.assigment

    def get_deadline(self):
        return self.deadline

    def get_status(self):
        return self.status

    def set_process(self, process_id):
        self.process = process_id

    def set_assigment(self, assigment_id):
        self.assigment = assigment_id

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_status(self, status):
        self.status = status

    def id(self, obj):
        return obj.id

    def __str__(self):
        return str(self.status) + " " + str(self.id)



class Document(models.Model):
    name = models.CharField(max_length=40, unique=False)
    version = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'))
    status = models.CharField(max_length=40, unique=False)
    date = models.DateField(default=django.utils.timezone.now)
    path = models.CharField(max_length=255,unique=False)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=2)
    type = models.CharField(max_length=40, unique=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, default=2)
    task = models.ForeignKey(Task,on_delete=models.SET(1) ,default=2)
    templateValues = models.CharField(max_length=256, unique=False)
    abstract = models.CharField(max_length=100, unique=False, default="document")
    keywords = models.CharField(max_length=100, unique=False, default="document")
    comment=models.CharField(max_length=255,unique=False,default="")

    def get_comment(self):
        return self.comment

    def set_comment(self,comment):
        self.comment=comment

    def get_abstract(self):
        return self.abstract

    def set_abstract(self,abstract):
        self.abstract = abstract

    def get_keywords(self):
        return self.keywords

    def set_keywords(self,keywords):
        self.keywords =keywords

    def id(self, obj):
        return obj.id

    def get_status(self):
        return self.status

    def get_name(self):
        return self.name

    def get_version(self):
        return self.version

    def get_date(self):
        return self.date

    def get_path(self):
        return self.path

    def get_owner(self):
        return self.owner

    def get_type(self):
        return self.type

    def get_template(self):
        return self.template

    def get_task(self):
        return self.task

    def get_template_values(self):
        return self.templateValues

    def set_status(self, status):
        self.status = status

    def set_name(self,name):
        self.name = name

    def set_version(self, version):
        self.version = version

    def set_date(self,date):
        self.date = date

    def set_path(self,path):
        self.path = path

    def set_owner(self, userId):
        self.owner = userId

    def set_type(self, type):
        self.type = type

    def set_template(self, template):
        self.template = template

    def set_task(self, task):
        self.task = task

    def set_template_values(self, templateValues):
        self.templateValues = templateValues


class Log(models.Model):
    user =  models.ForeignKey(MyUser, on_delete=models.CASCADE, default=2)
    action = models.CharField(max_length=255, unique=False)
    document_path =  models.CharField(max_length=255, unique=False)
    document_name =  models.CharField(max_length=255, unique=False)
    date = models.DateField(default=django.utils.timezone.now)

    def get_name(self):
        return self.name

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user =user

    def get_action(self):
        return self.action

    def set_action(self,action):
        self.action =action

    def get_document_path(self):
        return self.document_path

    def set_document_path(self, document_path):
        self.document_path = document_path

    def get_document_name(self):
        return self.name

    def set_document_name(self, document_name):
        self.document_name = document_name

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date =date



