from django.shortcuts import render
from .models import Ativo, HistAtivo
from users.models import User
from .forms import AtivoCreate, AtivoUpdate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
import json
from django.utils import timezone

#Index
def index(request):
    return render(request, 'index.html')

#List View | para listar Ativos e suas respectivas Infos
@login_required(login_url='/finhelp/login')
def profile(request):
    ativo = Ativo.objects.filter( fk_user = request.user.id )
    result = HistAtivo.objects.filter( fk_ativo__in = ativo, ultimo_hist = True)
    
    context = {
    'ativo_list': result,
    }

    return render(request, 'profile.html', context)

#Create View | para cadastrar ativos vinculado ao usuário
@login_required(login_url='/finhelp/login')
def create_ativo(request):
    flag = 0 #Flag para informar usuário de algum erro ou sucesso no cadastro

    if request.method == 'POST':
        form = AtivoCreate(request.POST)

        if form.is_valid():
            #ID do usuário
            user_id = User.objects.get(id=request.user.id)

            #Consome API HGBrasil https://hgbrasil.com/
            ativo = form.cleaned_data['b3'].upper()
            url = 'https://api.hgbrasil.com/finance/stock_price?key=5b52b69a&symbol=' + ativo
            request_api = requests.get(url).json()

            #Confirma se no retorno da API não consta erro
            if 'error' in request_api['results'][ativo]:
                flag = 1

            else:
                #Verifica se o usuário já cadastrou o ativo anteriormente
                if Ativo.objects.filter(fk_user__exact=user_id,b3__exact=ativo).count() == 0:
                    #Insere infos do ativo no banco de dados
                    ativo_insert = Ativo.objects.create(
                        b3= ativo,
                        nome_empresa= request_api['results'][ativo]['company_name'],
                        desc_empresa = request_api['results'][ativo]['description'],
                        lim_inf=form.cleaned_data['lim_inf'],
                        lim_sup=form.cleaned_data['lim_sup'],
                        fk_user = user_id,
                    )
                    ativo_insert.save()

                    #Dados para calcular valor anterior
                    percent = request_api['results'][ativo]['change_percent']
                    val = request_api['results'][ativo]['price']

                    #Calcula valor anterior
                    if percent == 0:
                        percent2 = 1
                    else:
                        percent2 = 1 + (percent / 100)

                    val_ant = round((val / percent2), 2)

                    #Insere valores do ativo no banco de dados
                    histAtivo = HistAtivo.objects.create(
                        fk_ativo = Ativo.objects.get(fk_user=user_id,b3=ativo),
                        valor =  val,
                        data_atualizacao = timezone.now(),
                        porcentagem = percent,
                        valor_anterior = round((val_ant / percent2),2),
                        ultimo_hist = True
                    )
                    histAtivo.save()

                    #Redireciona usuário para página profile
                    return HttpResponseRedirect(reverse('profile'))

                else:
                    flag = 3
    else:
        form = AtivoCreate()
        
    context = {
    'form': form,
    'flag': flag,
    }

    return render(request, 'finhelp/ativo/create.html', context)

#Update View | para atualizar limites de um determino ativo
@login_required(login_url='/finhelp/login')
def update_ativo(request, pk):
    ativo = get_object_or_404(Ativo, pk=pk)

    if request.method == 'POST':
        form = AtivoUpdate(request.POST)

        if form.is_valid():
            ativo.lim_sup = form.cleaned_data['lim_sup']
            ativo.lim_inf = form.cleaned_data['lim_inf']
            ativo.save()

            return HttpResponseRedirect(reverse('profile'))

    else:
        form = AtivoUpdate(initial={'lim_sup': ativo.lim_sup, 'lim_inf': ativo.lim_inf})
        
    context = {
    'form': form,
    'ativo': ativo,
    }

    return render(request, 'finhelp/ativo/update.html', context)

#Delete View | para deletar um determinado ativo
@login_required(login_url='/finhelp/login')
def delete_ativo(request, pk):
    ativo = get_object_or_404(Ativo, pk=pk)
    if request.method == 'POST':
        ativo.delete()
        return HttpResponseRedirect(reverse('profile'))

    context = {
    'ativo': ativo,
    }

    return render(request, 'finhelp/ativo/delete.html', context)

#List View | para listar históricos anteriores de um determinado ativo
@login_required(login_url='/finhelp/login')
def hist_ativo(request,pk):
    ativo = get_object_or_404(Ativo, pk=pk)
    hist_list = HistAtivo.objects.filter( fk_ativo__fk_user__id=request.user.id, fk_ativo=pk ).order_by('-data_atualizacao')
    
    context = {
    'hist_list': hist_list,
    'ativo': ativo
    }

    return render(request, 'finhelp/ativo/historico/historico.html', context)

