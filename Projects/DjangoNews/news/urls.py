from .views import HomePgeView
from django.urls import path
urlpatterns=[
    path('',HomePgeView.as_view(),name='home')
]