from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.Product.as_view()),
    path('product/<obj_id>', views.Product.as_view()),
]