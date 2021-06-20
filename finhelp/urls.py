from django.urls import path
from finhelp import views

urlpatterns = [
	#Index | Página principal
	path('', views.index, name='index'),
	
	#Urls para listar, cadastrar, atualizar e deletar ativos
	path('profile/ativo', views.profile, name='profile'),
	path('profile/ativo/create', views.create_ativo, name='ativo-create'),
	path('profile/ativo/update/<int:pk>', views.update_ativo, name='ativo-update'),
	path('profile/ativo/delete/<int:pk>', views.delete_ativo, name='ativo-delete'),
	path('profile/ativo/historico/<int:pk>', views.hist_ativo, name='ativo-hist'),
]
