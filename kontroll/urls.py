from django.urls import path
from kontroll import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('test/', views.test, name="test"),
    path('objects/<int:pk>/', views.obj_detail, name='obj_detail'),
]