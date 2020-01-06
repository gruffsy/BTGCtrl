from django.urls import path
from kontroll import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('objtr/<int:pk>/', views.objtr, name='objtr'),
    path('pdf/<int:pk>/', views.Pdf.as_view(), name='pdf'),
    path('avvik/<int:pk>/', views.avvik, name='avvik'),
]
