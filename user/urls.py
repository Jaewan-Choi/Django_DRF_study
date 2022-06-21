from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', views.UserApiView.as_view()),
    path('logout/', views.UserApiView.as_view()),
    path('blog/', include('blog.urls')),
]