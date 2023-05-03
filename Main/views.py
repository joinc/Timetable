from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from Main.tools import get_profile

######################################################################################################################


def index(request):
    """
    Отображение главной страницы
    :param request:
    :return: HttpResponse
    """
    context = {
        'title': 'Главная',
        'current_profile': get_profile(user=request.user) if request.user.is_authenticated else None,
    }
    return render(request=request, template_name='index.html', context=context)


######################################################################################################################


def login(request) -> HttpResponse:
    """
    Вход пользователя
    :param request:
    :return: HttpResponse
    """
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect(request.POST['next'])
        else:
            messages.error(request, 'Введены не правильные учетные данные')
            return redirect(reverse('login'))
    else:
        context = {
            'title': 'Авторизация',
            'next': request.GET.get('next') if request.GET.get('next') else settings.SUCCESS_URL,
        }
        return render(request=request, template_name='login.html', context=context, )


######################################################################################################################


@login_required
def logout(request) -> HttpResponse:
    """
    Выход пользователя
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect(reverse('index'))


######################################################################################################################
