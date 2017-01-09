from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect

from DocumentsFlowApp.models import Document, MyUser
from .forms import UploadFileForm

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

import datetime


def index(request):
    return render(request, "login.djt")


@csrf_protect
def homepage(request):
    print("here")
    c = {}
    c.update(csrf(request))
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)

        return render(request, "homepage.html", c)
    else:
        return redirect("/")


def logout_user(request):
    logout(request)
    return redirect("/")

def add_uploaded_file(request,file):

    # for item in Document.objects.all():
    #     item.delete()

    d = Document()
    ok = False
    for item in Document.objects.all():
        if item.get_owner().username == request.user.username and item.get_path() == "D:/Patricia/Anul3/ProiectColectiv-Team/DocumentsFlow/resources"+ "/" + request.user.username + file.name:
            if item.get_status() == "DRAFT":
                item.set_version(item.get_version() + 0.1)
                default_storage.delete(item.get_path())
                path =  default_storage.save(item.get_path(), file)
                item.set_path(path)
                item.set_date(datetime.datetime.now())
                item.save()
                ok = True

            if item.get_status() == "FINAL":
                item.set_version(item.get_version() + 1.0)
                default_storage.delete(item.get_path())
                path = default_storage.save(item.get_path(), file)
                item.set_path(path)
                item.set_date(datetime.datetime.now())
                item.save()
                ok = True
            break


    if ok == False:
        d.set_name(file.name)
        d.set_version(0.1)
        d.set_owner(request.user)
        d.set_status("DRAFT")
        d.set_date(datetime.datetime.now())
        path = default_storage.save(
            "D:\Patricia\Anul3\ProiectColectiv-Team\DocumentsFlow\\resources" + "\\" + request.user.username + file.name ,
            file)
        d.set_path(path)
        d.save()

    for item in Document.objects.all():
        print(item.get_path())
        print(item.get_version())


@csrf_protect
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            add_uploaded_file(request, request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, "uploadFile.html", {'form': form})