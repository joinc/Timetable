from django.shortcuts import render

######################################################################################################################


def index(request):
    """
    Отображение главной страницы
    :param request:
    :return: HttpResponse
    """
    context = {
        'title': 'Главная',
    }
    return render(request=request, template_name='index.html', context=context)


######################################################################################################################
