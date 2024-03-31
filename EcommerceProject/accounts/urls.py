from django.urls import path
from .views import (
    SignUpView,
    LoginView,
    LogoutView,
    AccountDetailView,
    ProfieDetailView
                    )
urlpatterns=[
    path('sign_up/',SignUpView.as_view(),name='registration'),
    path('log_in/',LoginView,name='log_in'),
    path('log_out/',LogoutView,name='log_out'),
    path('account/',AccountDetailView.as_view(),name='account_detail'),
    path('account/profile/',ProfieDetailView.as_view(),name='profile_detail')
]