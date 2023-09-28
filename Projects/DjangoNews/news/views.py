from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
# Create your views here.
class HomePgeView(ListView):
    model=Post
    template_name='home.html'
