# -*- coding: utf-8 -*-

from django.shortcuts import redirect, reverse

######################################################################################################################


def superuser_only(function):
    """
    Декоратор, проверят, что-бы пользователь обладал правами суперпользователя
    :param function:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return function(request, *args, **kwargs)
            else:
                return redirect(reverse('index'))
        return redirect(reverse('login'))
    return wrapper


######################################################################################################################