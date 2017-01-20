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
    url(r'^delete_draft/', views.delete_draft, name='delete_draft'),
    url(r'^createFile/', views.create_file, name='create_file'),
    url(r'^download', views.download_file, name='download_file'),
    url(r'^editMetadata/', views.edit_metadata, name='editMetadata'),
    url(r'^processes/', views.processes, name='processes'),
    url(r'^process/', views.process, name='process'),
    url(r'^add_document_to_process/', views.add_document_to_process, name = 'add_document_to_process'),
    url(r'^start_process/', views.start_process, name='start_process'),
    url(r'^zona_taskuri_initiate/', views.zona_taskuri_initiate, name='zona_taskuri_initiate'),
    url(r'^zona_taskuri/', views.zona_taskuri, name='zona_taskuri'),
    url(r'^logs/', views.logs, name='logs'),
    url(r'^accept_task/', views.accept_task, name='accept_task'),

]

urlpatterns += staticfiles_urlpatterns()
