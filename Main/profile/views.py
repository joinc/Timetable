# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from Main.models import UserProfile
from Main.decorators import superuser_only
from Main.tools import get_profile, check_password
from Main.profile.forms import FormProfile, FormPassword

######################################################################################################################


@login_required
def profile_list(request):
    """
    Список пользователей
    :param request:
    :return:
    """
    current_profile = get_profile(user=request.user)
    context = {
        'current_profile': current_profile,
        'profile_edit': current_profile.user.is_superuser,
        'title': 'Список пользователей',
        'list_breadcrumb': (),
        'list_profile': UserProfile.objects.all(),
    }
    return render(request=request, template_name='profile/list.html', context=context, )


######################################################################################################################


@superuser_only
def profile_create(request):
    """
    Добавление пользователя
    :param request:
    :return:
    """
    if request.POST:
        form_profile = FormProfile(request.POST)
        username = form_profile['username'].value()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        initial = {
            'username': username,
            'first_name': form_profile['first_name'].value(),
            'last_name': form_profile['last_name'].value(),
        }
        message_list = check_password(username=username, password=password, password2=password2)
        if form_profile.is_valid() and not message_list:
            user = form_profile.save()
            user.set_password(password)
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user, )
            profile.save()
            messages.success(request, f'Пользователь {profile} успешно создан.')
            # return redirect(reverse('profile_show', args=(profile.id, )))
            return redirect(reverse('profile_list'))
        else:
            if User.objects.filter(username=username).exists():
                del initial['username']
                message_list.append(f'Пользователь {username} уже существует.')
        for message in message_list:
            messages.error(request, message)
        form_profile = FormProfile(
            initial=initial,
        )
    else:
        form_profile = FormProfile()
    context = {
        'current_profile': get_profile(user=request.user),
        'title': 'Добавление нового пользователя',
        'list_breadcrumb': (
            (reverse('profile_list'), 'Список пользователей'),
        ),
        'form_profile': form_profile,
        'form_password': FormPassword(),
    }
    return render(request=request, template_name='profile/create.html', context=context, )


######################################################################################################################


@login_required
def profile_show(request, profile_id):
    """
    Страница профиля пользователя
    :param request:
    :param profile_id:
    :return:
    """
    current_profile = get_profile(user=request.user)
    profile = get_profile(profile=profile_id)
    if request.POST and (current_profile == profile or current_profile.user.is_superuser):
        form_password = FormPassword(request.POST)
        password = form_password['password'].value()
        password2 = form_password['password2'].value()
        message_list = check_password(username=profile.user.username, password=password, password2=password2)
        if message_list:
            for message in message_list:
                messages.error(request, message)
        else:
            messages.success(request, f'Пароль пользователя {profile} успешно изменен.')
            profile.user.set_password(password)
            profile.user.save()
            if current_profile == profile:
                user = auth.authenticate(username=current_profile.user.username, password=password)
                if user:
                    auth.login(request, user)
                else:
                    messages.error(request, 'Введены не правильные учетные данные')
                    return redirect(reverse('login'))
            return redirect(reverse('profile_show', args=(profile.id, )))
    context = {
        'current_profile': current_profile,
        'profile_edit': current_profile.user.is_superuser,
        'title': profile,
        'list_breadcrumb': (
            (reverse('profile_list'), 'Список пользователей'),
        ),
        'form_password': FormPassword(),
        'profile': profile,
    }
    return render(request=request, template_name='profile/show.html', context=context, )


######################################################################################################################


@superuser_only
def profile_edit(request, profile_id):
    """
    Страница профиля пользователя
    :param request:
    :param profile_id:
    :return:
    """
    profile = get_profile(profile=profile_id)
    if request.POST:
        form_profile = FormProfile(request.POST)
        profile.user.first_name = form_profile['first_name'].value()
        profile.user.last_name = form_profile['last_name'].value()
        profile.user.save()
        messages.success(request, f'Пользователь {profile} успешно отредактирован и сохранен', )
        return redirect(reverse('profile_show', args=(profile.id, )))
    else:
        form_profile = FormProfile(instance=profile.user, )
    context = {
        'current_profile': get_profile(user=request.user),
        'title': f'Редактирование пользователя {profile}',
        'list_breadcrumb': (
            (reverse('profile_list'), 'Список пользователей'),
            (reverse('profile_show', args=(profile.id, )), profile),
        ),
        'form_profile': form_profile,
    }
    return render(request=request, template_name='profile/edit.html', context=context, )


######################################################################################################################


@superuser_only
def profile_blocked(request, profile_id):
    """
    Функция по блокировке или разблокировки профиля пользователя в зависимости от состояния
    :param request:
    :param profile_id:
    :return:
    """
    profile = get_profile(profile=profile_id)
    if profile.blocked:
        profile.unblock()
        messages.info(request, f'Пользователь {profile} разблокирован', )
    else:
        profile.block()
        messages.error(request, f'Пользователь {profile} заблокирован', )
    return redirect(reverse('profile_show', args=(profile_id, )))


######################################################################################################################
