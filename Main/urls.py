from django.urls import path
from Main import views

urlpatterns = [
    path('', views.index, name='index', ),
    # path('login/', views.login, name='login', ),
    # path('logout/', views.logout, name='logout', ),
]
