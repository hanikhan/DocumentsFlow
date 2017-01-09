from django.conf.urls import url
from django.contrib.auth.views import login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^homepage/', views.homepage, name='homepage'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^uploadFile/', views.upload_file, name='uploadFile')
]

urlpatterns += staticfiles_urlpatterns()
