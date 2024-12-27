from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('visao-geral/', views.visao_geral),
]
