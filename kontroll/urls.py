from django.urls import path
from kontroll import views

urlpatterns = [
    path('', views.index, name='index'),
]