from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.Article.as_view()),
    path('post/<obj_id>', views.Article.as_view()),
]