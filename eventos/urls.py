from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lista/', views.lista_eventos, name='lista'),
    path('<int:pk>/', views.detalhe_evento, name='detalhe'),
    path('novo/', views.novo_evento, name='novo'),
    path('<int:pk>/editar/', views.editar_evento, name='editar'),
    path('<int:pk>/excluir/', views.excluir_evento, name='excluir'),
]
