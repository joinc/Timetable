# -*- coding: utf-8 -*-

from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from Main.models import UserProfile

######################################################################################################################


def get_profile(profile=None, user=None) -> UserProfile:
    """
    Получение профиля пользователя
    :param profile:
    :param user:
    :return: UserProfile
    """
    if profile:
        return get_object_or_404(UserProfile, id=profile)
    if user:
        return get_object_or_404(UserProfile, user=user)
    return HttpResponseNotFound()


######################################################################################################################


def check_password(username, password, password2):
    """
    Проверка выполнения требований к паролю
    :param username:
    :param password:
    :param password2:
    :return:
    """
    message_list = []
    if password != password2:
        message_list.append('Пароли не совпадают.')
    if len(password) < 8:
        message_list.append('Длина пароля менее 8 символов.')
    if password.isdigit():
        message_list.append('Пароль состоит только из цифр.')
    if password == username:
        message_list.append('Пароль совпадает с логином.')
    return message_list


######################################################################################################################
