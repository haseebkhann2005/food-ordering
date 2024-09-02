"""
URL configuration for food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,re_path,include
from products.views import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', home , name="home"),
    path('login/', p_login , name="p_login"),
    path('logout/',logout_page,name="logout_page"),
    path('register/', p_register , name="p_register"),
    path('contact/', contact  , name="contact"),
    path('about/', about  , name="about"),
    path('menu/', menu  , name="menu"),
    path('blog/', blog  , name="blog"),
    path('top-5/', top5  , name="top5"),
    path('health-tips/',h_tips,name = "h_tips"),
    path('guide/',guide,name = "guide"),
    path('add-meal/',add_meal,name = "add_meal"),
    path('reviews/',reviews,name = "reviews"),
    path('delete-meal/<id>/',delete_meal,name="delete_meal"),
    path('auth/', include('social_django.urls', namespace='social')),

    path('purchase/<uuid:product_id>/', purchase_item, name='purchase_item'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()