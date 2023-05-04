from django.urls import path
from Main import views
from Main.profile import views as profile

urlpatterns = [
    path('', views.index, name='index', ),
    path('login/', views.login, name='login', ),
    path('logout/', views.logout, name='logout', ),
    path('profile/list/', profile.profile_list, name='profile_list', ),
    path('profile/create/', profile.profile_create, name='profile_create', ),
    path('profile/<int:profile_id>/show/', profile.profile_show, name='profile_show', ),
    path('profile/<int:profile_id>/edit/', profile.profile_edit, name='profile_edit', ),
    path('profile/<int:profile_id>/blocked/', profile.profile_blocked, name='profile_blocked', ),
]
