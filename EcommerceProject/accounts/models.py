from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Customer(AbstractUser):
    date_of_birth=models.DateField(null=True,blank=True)
    phone_number=PhoneNumberField()