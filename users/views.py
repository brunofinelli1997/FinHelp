from django.shortcuts import render
from .models import User
from .forms import UserCreate, UserUpdate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

#Create View | para cadastrar usuário
def create_user(request):
    flag = 0
    if request.method == 'POST':
        form = UserCreate(request.POST)

        if form.is_valid():
            #Insere dados do formulário no banco
            users = User.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                username=form.cleaned_data['username'],
                profession=form.cleaned_data["profession"],
            )
            users.set_password(form.cleaned_data["password1"])
            users.save()

            flag = 1
            form = UserCreate()

    else:
        form = UserCreate()
        
    context = {
    'form': form,
    'flag' : flag,
    }

    return render(request, 'finhelp/user/create.html', context)

#Update View | para atualizar cadastro do usuário
@login_required(login_url='/finhelp/login')
def update_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdate(request.POST)

        if form.is_valid():
            #Insere dados do formulário no banco
            user.first_name=form.cleaned_data["first_name"]
            user.last_name=form.cleaned_data["last_name"]
            user.email=form.cleaned_data["email"]
            user.profession=form.cleaned_data["profession"]
            user.save()

            return HttpResponseRedirect(reverse('profile'))

    else:
        form = UserUpdate(initial={
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'username': user.username,
            'profession': user.profession,
            })
        
    context = {
    'form': form,
    }

    return render(request, 'finhelp/user/update.html', context)
