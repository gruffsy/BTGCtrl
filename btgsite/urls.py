"""btgsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from kontroll import views

router = routers.DefaultRouter()
router.register(r'objects', views.ObjectViewSet)
router.register(r'objtrs', views.ObjTrViewSet)
router.register(r'avviks', views.AvvikViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'months', views.MonthViewSet)
router.register(r'slokketypes', views.ObjTrViewSet)
router.register(r'extinguishants', views.ExtinguishanttViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kontroll.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
