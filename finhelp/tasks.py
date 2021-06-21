#Agendar job
from apscheduler.schedulers.background import BackgroundScheduler

#Models Importados
from .models import Ativo, HistAtivo
from users.models import User

#Consumo da API
import requests
import json

#Consultar data e hora local
from django.utils import timezone

#Envio dos e-mails
from django.core.mail import send_mail


#Job para atualizar infos dos ativos
def update_histAtivo():
    #Consulta quais ativos os clientes estao monitorando
    b3_list = Ativo.objects.values('b3').distinct()

    for b3 in b3_list:
        ativo = b3['b3']
        #Consulta as últimas infos que foram cadastradas no banco de dados
        hist_list = HistAtivo.objects.filter( fk_ativo__b3 = ativo, ultimo_hist=True)
        
        #Consome API
        url = 'https://api.hgbrasil.com/finance/stock_price?key=5b52b69a&symbol=' + ativo
        request_api = requests.get(url).json()

        percent = request_api['results'][ativo]['change_percent']
        val = request_api['results'][ativo]['price']

        #Calcula valor anterior
        if percent == 0:
            percent2 = 1
        else:
            percent2 = 1 + (percent / 100)

        valor_anterior = round((val / percent2), 2)
            
        #Atualiza as infos dos ativos
        for hist in hist_list:
            histAtivo = HistAtivo.objects.create(
                fk_ativo = hist.fk_ativo,
                valor =  val,
                data_atualizacao = timezone.now(),
                porcentagem = percent,
                valor_anterior = round((valor_anterior / percent2),2),
                ultimo_hist = True
            )
            histAtivo.save()

            #Retira flag do histórico passado
            hist.ultimo_hist = False
            hist.save()

    print('Historico dos ativos atualizado...')

#Job para envio de e-mail caso exista possibilidade de venda ou compra de ativos
def send_emails():
    #Consulta todos os usuários
    user_list = User.objects.all()

    for user in user_list:
        #Consulta as últimas infos dos ativos do usuario
        hist_list = HistAtivo.objects.filter(ultimo_hist=True, fk_ativo__fk_user__id__exact=user.id)

        #Variáveis para operações
        ativos_compra = ''
        ativos_venda = ''
        email_cliente = ''

        for hist in hist_list:
            #Possibilidade de compra de ativo
            if hist.valor < hist.fk_ativo.lim_inf:
                ativos_compra += hist.fk_ativo.b3 + ' '
                
            #Possibilidade de venda de ativo
            elif hist.valor > hist.fk_ativo.lim_sup:  
                ativos_venda += hist.fk_ativo.b3 + ' '
                
        #Envia e-mails
        if len(ativos_compra) > 0:
            send_mail(
            'Oportunidade de compra de ativo | Finhelp',
            'Ola prezado cliente, \n\n' + 'O(s) ativo(s) ' + ativos_compra +'esta(o) com oportunidade de compra!!\n\n' + 'Atenciosamente,\n\n' + 'Equipe Finhelp',
            'contato@finhelp.com.br',
            [user.email],
            fail_silently=False,
            )
        if len(ativos_venda) > 0:
            send_mail(
            'Oportunidade de venda de ativo | Finhelp',
            'Ola prezado cliente, \n\n' + 'O(s) ativo(s) ' + ativos_venda +'esta(o) com oportunidade de venda!!\n\n' + 'Atenciosamente,\n\n' + 'Equipe Finhelp',
            'contato@finhelp.com.br',
            [user.email],
            fail_silently=False,
            )

    print("E-mails enviados...")

#Define quando os jobs serão executados
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_histAtivo, "interval", minutes = 1)
    scheduler.add_job(send_emails, "interval",  minutes = 1)
    scheduler.start()
