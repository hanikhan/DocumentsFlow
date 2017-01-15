from django.conf.urls import url
from django.contrib.auth.views import login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^homepage/', views.homepage, name='homepage'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^uploadFile/', views.upload_file, name='uploadFile'),
    url(r'^zona_de_lucru/', views.zona_de_lucru, name='zona_de_lucru'),
    url(r'^change_document_status_to_final/', views.change_document_status_to_final, name='change_document_status_to_final'),
    url(r'^change_document_status_to_draft/', views.change_document_status_to_draft, name='change_document_status_to_draft'),
    url(r'^delete_draft/', views.delete_draft, name='delete_draft')
]

urlpatterns += staticfiles_urlpatterns()
