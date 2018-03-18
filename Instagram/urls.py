from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('like/', views.like, name='like'),
    path('leave_comment/', views.leave_comment, name='leave_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
    path('<str:username>/', views.my_page, name='my_page'),
]
