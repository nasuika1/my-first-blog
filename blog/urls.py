from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.post_list, name = 'post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/',views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
=======
    path('', views.home, name = 'home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/',views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('dearpoint/', views.dearpoint, name='dearpoint')
>>>>>>> 親愛度計算を追加
]