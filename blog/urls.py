from django.urls import path
from . import views

urlpatterns = [
    path('mypost/', views.Mypost.as_view()),
]