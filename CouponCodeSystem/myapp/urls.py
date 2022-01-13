from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('neworder', views.neworder, name='neworder'),
    path('vieworder', views.vieworder, name='vieworder'),
    path('viewcoupon', views.viewcoupon, name='viewcoupon'),
    path('newcoupon', views.newcoupon, name='newcoupon'),
    path('editcoupon/<str:pk>', views.editcoupon, name='editcoupon'),
    path('delcoupon/<str:pk>', views.delcoupon, name='delcoupon'),
]
