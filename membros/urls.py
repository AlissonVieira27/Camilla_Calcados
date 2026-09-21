from django.urls import include, path
from . import views

urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.home, name='home'),
    path('bibliotecas/', views.listar_bibliotecas, name='listar_bibliotecas'),
    path('bibliotecas/criar/', views.criar_biblioteca, name='criar_biblioteca'),
    path('bibliotecas/editar/<int:id>/', views.editar_biblioteca, name='editar_biblioteca'),
    path('bibliotecas/deletar/<int:id>/', views.deletar_biblioteca, name='deletar_biblioteca'),
    path('bibliotecas/favoritar/<int:id>/', views.alternar_favorito, name='alternar_favorito'),
    path('salvos/', views.salvos, name='salvos'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('ajuda/', views.ajuda, name='ajuda'),
    path('termos/', views.termos, name='termos'),
    path('privacidade/', views.privacidade, name='privacidade'),
]
