from django.contrib import admin
from .models import Ativo, HistAtivo

#Registrando models para painel Admin
admin.site.register(Ativo)
admin.site.register(HistAtivo)