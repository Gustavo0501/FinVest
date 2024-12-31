from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('visao-geral/', views.visao_geral),
    path('acoes/', views.stock_table),
    path('criptomoedas/', views.criptomoedas),
    path('graficos/', views.graficos),
]
