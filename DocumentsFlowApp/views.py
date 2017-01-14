from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect

from DocumentsFlowApp.models import Document, MyUser, Task
from .forms import UploadFileForm

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
import datetime

from DocumentsFlowApp.models import Document
from decimal import Decimal
from django.core.mail import send_mail

def index(request):
    return render(request, "login.djt")


@csrf_protect
def homepage(request):
    print("******* " + str(request))
    c = {}
    c.update(csrf(request))
    if "user" not in str(request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return render(request, "homepage2.html", c)
    else:
        print("here")
        return render(request, "homepage2.html", c)


@login_required
@csrf_protect
def zona_de_lucru(request):
    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()
    print(docs)
    print(request.user)
    for doc in docs:
        if doc.get_owner().username == request.user.username:
            wasDeleted = deleteDocumentAfter30(request,doc)
            if wasDeleted ==True:
                continue;
            if doc.get_task().id == 1:
                user_docs.append(doc)
    c["docs"] = user_docs
    return render(request, "zona_de_lucru.html", c)

def deleteDocumentAfter30(request,document):
    if  (datetime.datetime.now().date() - document.get_date()).days > 30:
        send_mail("Delete","The file "+document.get_name() + " with version " + str(document.get_version()) +" will be deleted in 30 days","websmarts2017@gmail.com",[request.user.email],fail_silently=False)
        return False
    elif (datetime.datetime.now().date() - document.get_date()).days > 60:
        send_mail("Delete",
                  "The file " + document.get_name() + " with version " + str(document.get_version()) + " was deleted",
                  "websmarts2017@gmail.com", [request.user.email], fail_silently=False)
        document.delete()
        default_storage.delete(document.get_path())
        return True
    return False

@csrf_protect
def change_document_status_to_final(request):
    c = {}
    c.update(csrf(request))


    document_path = request.POST.get("document_path")
    print(document_path)
    document = Document.objects.filter(path=document_path).first()
    document.set_status("FINAL")
    document.set_version(1.0)
    document.save()

    user_docs = []
    docs = Document.objects.all()

    for doc in docs:
        if doc.get_owner().username == request.user.username:
            if doc.get_task().id == 1:
                user_docs.append(doc)
    c["docs"] = user_docs
    return render(request, "zona_de_lucru.html", c)


def logout_user(request):
    logout(request)
    return redirect("/")


def add_uploaded_file(request,file):

    #
    # for item in Document.objects.all():
    #     item.delete()

    d = Document()
    ok = False
    for item in Document.objects.all():
        print(item.get_path())
        print("D:\Patricia\Anul3\ProiectColectiv-Team\DocumentsFlow\\resources"+ "/" + request.user.username + file.name)
        if item.get_owner().username == request.user.username and item.get_path() == "D:/Patricia/Anul3/ProiectColectiv-Team/DocumentsFlow/resources"+ "/" + request.user.username + file.name:
            if item.get_status() == "DRAFT":
                item.set_version(item.get_version() + Decimal('0.1'))
                default_storage.delete(item.get_path())
                path = default_storage.save(item.get_path(), file)
                item.set_path(path)
                item.set_date(datetime.datetime.now())
                ts = Task.objects.all()
                for t in ts:
                    if t.id == 1:
                        item.set_task(t)
                        break
                item.save()
                ok = True

            if item.get_status() == "FINAL":
                item.set_version(item.get_version() + Decimal('1.0'))
                default_storage.delete(item.get_path())
                path = default_storage.save(item.get_path(), file)
                item.set_path(path)
                item.set_date(datetime.datetime.now())
                ts = Task.objects.all()
                for t in ts:
                    if t.id == 1:
                        item.set_task(t)
                        break
                item.save()
                ok = True
            break


    if ok == False:
        d.set_name(file.name)
        d.set_version(0.1)
        d.set_owner(request.user)
        d.set_status("DRAFT")
        d.set_date(datetime.datetime.now())
        ts = Task.objects.all()
        for t in ts:
            if t.id == 1:
                d.set_task(t)
                break
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
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            add_uploaded_file(request, request.FILES['file'])
            return render(request, "homepage2.html", c)
    else:
        form = UploadFileForm()
    return render(request, "uploadFile.html", {'form': form})