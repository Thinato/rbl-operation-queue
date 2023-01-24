from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('registro/', views.registro, name='registro'),
    path('registro/nova_peca', views.nova_peca, name='nova_peca'),
    path('registro/peca/<str:index>', views.editar_peca, name='editar_peca'),
    path('registro/peca/<str:index>/ops', views.operacoes, name='operacoes'),
    path('registro/maquina/<int:index>', views.editar_maquina, name='editar_maquina'),
    path('registro/maquina', views.nova_maquina, name='nova_maquina'),
    path('fila/', views.fila, name='fila'),
    path('instancia', views.instancia, name='instancia'),
    path('search', views.search, name='search'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/novo', views.novo_pedido, name='novo_pedido'),
    path('pedidos/atualizar/<int:index>', views.atualizar_pedido, name='atualizar_pedido'),
    
]