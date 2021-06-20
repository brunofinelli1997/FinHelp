# Finhelp
Desafio proposto pela INOA SISTEMAS, os requisitos do desafio:
- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável, para consulta posterior
- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo
- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior

## Dependêcias
Para executar o projeto instale as seguintes dependências:
```sh
pip install django
```
```sh
pip install django-crispy-forms
```
```sh
pip install requests
```
```sh
pip install apscheduler
```
## Prompt de Comando
Precisamos utlizar dois prompts, um para executar a aplicação e o outro para executar o servidor SMTP
```sh
python manage.py runserver
```
```sh
python -m smtpd -n -c DebuggingServer localhost:1025
```

## Login
Foi criado um super usuário para acessar o /admin
```sh
usuário: inoa
senha: inoa#2021
```
