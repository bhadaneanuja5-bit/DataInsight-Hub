from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'upload/',
        views.upload_dataset,
        name='upload_dataset'
    ),

    path(
        'datasets/',
        views.dataset_list,
        name='dataset_list'
    ),

    path(
        'analysis/<int:dataset_id>/',
        views.dataset_analysis,
        name='dataset_analysis'
    ),

]