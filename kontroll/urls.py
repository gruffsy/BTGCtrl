from django.urls import path
from kontroll import views, forms


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('test/', views.test, name="test"),
    path('objects/<int:pk>/', views.obj_detail, name='obj_detail'),
    path('objtr/<int:pk>/', views.objtr, name='objtr'),
    path('pdf/<int:pk>/', views.Pdf.as_view(), name='pdf'),
    path('contact/', forms.nyslokketype, name='nyslokketype'),
    path('nyobject/<int:pk>', views.nyobject, name='nyobject'),

]