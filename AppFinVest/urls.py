from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    #path('recipes/<int:id>/', views.recipe),
]
