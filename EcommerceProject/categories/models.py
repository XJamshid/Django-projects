from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=50)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'slug':self.slug})