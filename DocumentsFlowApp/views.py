import io
import os

from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.static import serve

from DocumentsFlowApp.models import Document, MyUser, Task, Template
from utils import get_project_path_forward_slash, get_project_path
from .forms import UploadFileForm
from .forms import CreateFileForm

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
import datetime
from DocumentsFlowApp.models import Document
from DocumentsFlowApp.models import Log
from DocumentsFlowApp.models import *
from decimal import Decimal
from django.core.mail import send_mail

from docx import Document as WordDocument


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
    print(request.user)
    for doc in docs:
        if doc.get_owner().username == request.user.username and doc.get_task().id == 1:
            wasDeleted = deleteDocumentAfter30(request, doc)
            if wasDeleted == True:
                continue
            if doc.get_task().id == 1:
                user_docs.append(doc)
    c["docs"] = user_docs
    return render(request, "zona_de_lucru.html", c)


def deleteDocumentAfter30(request, document):
    if (datetime.datetime.now().date() - document.get_date()).days > 30:
        log = Log()
        log.set_date(datetime.datetime.now().date())
        log.set_action("PROGRAMAT PENTRU STERGERE")
        log.set_document_name(document.get_name())
        log.set_document_path(document.get_path())
        log.set_user(document.get_owner())
        log.save()

        send_mail("Delete", "The file " + document.get_name() + " with version " + str(
            document.get_version()) + " will be deleted in 30 days", "websmarts2017@gmail.com", [request.user.email],
                  fail_silently=False)
        return False
    elif (datetime.datetime.now().date() - document.get_date()).days > 60:
        log = Log()
        log.set_date(datetime.datetime.now().date())
        log.set_action("STERGERE DOCUMENT")
        log.set_document_name(document.get_name())
        log.set_document_path(document.get_path())
        log.set_user(document.get_owner())
        log.save()

        send_mail("Delete",
                  "The file " + document.get_name() + " with version " + str(document.get_version()) + " was deleted",
                  "websmarts2017@gmail.com", [request.user.email], fail_silently=False)
        document.delete()
        default_storage.delete(document.get_path())
        return True
    return False


@csrf_protect
def change_document_status_to_final(request):
    document_path = request.GET.get("path")
    document = Document.objects.filter(path=document_path).first()
    document.set_status("FINAL")
    document.set_version(1.0)
    document.save()


    log = Log()
    log.set_date(datetime.datetime.now().date())
    log.set_action("MAKE DOCUMENT FINAL")
    log.set_document_name(document.get_name())
    log.set_document_path(document.get_path())
    log.set_user(document.get_owner())
    log.save()

    c = {}
    c.update(csrf(request))
    return render(request, "homepage2.html", c)


@csrf_protect
def change_document_status_to_draft(request):
    document_path = request.GET.get("path")
    document = Document.objects.filter(path=document_path).first()
    document.set_status("DRAFT")
    document.set_version(0.1)
    document.save()

    log = Log()
    log.set_date(datetime.datetime.now().date())
    log.set_action("MAKE DOCUMENT DRAFT")
    log.set_document_name(document.get_name())
    log.set_document_path(document.get_path())
    log.set_user(document.get_owner())
    log.save()

    c = {}
    c.update(csrf(request))
    return render(request, "homepage2.html", c)


@csrf_protect
def delete_draft(request):
    document_path = request.POST.get("document_path")
    document_path = document_path.replace("\\", "\\\\")
    document = Document.objects.filter(path=document_path).first()
    log = Log()
    log.set_date(datetime.datetime.now().date())
    log.set_action("STERGERE DRAFT")
    log.set_document_name(document.get_name())
    log.set_document_path(document.get_path())
    log.set_user(document.get_owner())
    log.save()
    document.delete()
    default_storage.delete(document.get_path())

    c = {}
    c.update(csrf(request))
    return render(request, "homepage2.html", c)


def logout_user(request):
    logout(request)
    return redirect("/")


def add_uploaded_file(request, file, abstract, keywords):

      # for item in Document.objects.all():
      #     item.delete()


    ok = False
    print(get_project_path_forward_slash())
    for item in Document.objects.all():
        path = item.get_path().split("^", 1)
        if item.get_owner().username == request.user.username \
                and get_project_path_forward_slash() + "resources/" + path[1] == \
                    get_project_path_forward_slash() + "resources" + "/" + request.user.username + file.name:
            if item.get_status() == "DRAFT":
                doc = Document.objects.filter(name=file.name).last()
                newDocument = Document()
                newDocument.set_name(file.name)
                newDocument.set_status("DRAFT")
                newDocument.set_version(doc.get_version() + Decimal('0.1'))
                newDocument.set_date(datetime.datetime.now())
                newDocument.set_owner(request.user)
                path = default_storage.save(get_project_path_forward_slash() + "resources/" +
                                            str(newDocument.get_version()) + "^" + path[1], file)
                print("*******" + str(path))
                newDocument.set_path(path)
                ts = Task.objects.all()
                for t in ts:
                    if t.id == 1:
                        newDocument.set_task(t)
                        break

                newDocument.set_abstract(abstract)
                newDocument.set_keywords(keywords)

                log = Log()
                log.set_date(datetime.datetime.now().date())
                log.set_action("UPLOAD DOCUMENT")
                log.set_document_name(newDocument.get_name())
                log.set_document_path(newDocument.get_path())
                log.set_user(newDocument.get_owner())
                log.save()

                newDocument.save()
                ok = True
                break

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

                item.set_abstract(abstract)
                item.set_keywords(keywords)

                log = Log()
                log.set_date(datetime.datetime.now().date())
                log.set_action("UPLOAD DOCUMENT")
                log.set_document_name(item.get_name())
                log.set_document_path(item.get_path())
                log.set_user(item.get_owner())
                log.save()

                item.save()
                ok = True
            break

    if ok == False:
        d = Document()
        d.set_name(file.name)
        d.set_version(0.1)
        d.set_owner(request.user)
        d.set_status("DRAFT")
        d.set_date(datetime.datetime.now())
        d.set_keywords(keywords)
        d.set_abstract(abstract)
        ts = Task.objects.all()
        for t in ts:
            if t.id == 1:
                d.set_task(t)
                break
        path = default_storage.save(
            get_project_path() + "resources" + "\\" + str(d.get_version()) + "^" + request.user.username + file.name,
            file)
        d.set_path(path)

        log = Log()
        log.set_date(datetime.datetime.now().date())
        log.set_action("UPLOAD DOCUMENT")
        log.set_document_name(d.get_name())
        log.set_document_path(d.get_path())
        log.set_user(d.get_owner())
        log.save()

        d.save()


@csrf_protect
def upload_file(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.POST.get('abstract'))
        if form.is_valid():
            add_uploaded_file(request, request.FILES['file'],request.POST.get('abstract'),request.POST.get('keywords'))
            return render(request, "homepage2.html", c)
    else:
        form = UploadFileForm()
    return render(request, "uploadFile.html", {'form': form})


def approve_task(document_id):
    document = Document.objects.filter(document_id=document_id).first()
    task = document.get_task()
    next_step = task.get_step()+1

    assignment_id = task.get_assigment().id

    process_id = task.get_process().id

    create_task_for_process(assignment_id,process_id,next_step)

def accept_task(request):
    task_id = int(request.GET.get("task_id"))
    task = Task.objects.filter(id=int(task_id)).first()
    task.set_status("ACCEPTED")
    flux = task.get_process().get_flux()
    counter = 0
    for assig in Assigment.objects.all():
        if assig.get_flux() == flux:
            counter +=1

    if task.get_step() != counter:
        start_task_for_step(task.get_process().id,task.get_step()+1)
    else:
        for doc in Document.objects.all():
            if doc.get_user() == task.get_process().get_owner():
                doc.set_status("BLOCAT")
                doc.save()

    return zona_taskuri(request)

def respinge_task(request):

    task_id = int(request.GET.get("task_id"))
    task = Task.objects.filter(id=int(task_id)).first()
    task.set_status("REJECTED")

    for doc in Document.objects.all():
        if doc.get_user() == task.get_process().get_owner():
            doc.set_status("BLOCAT")
            doc.save()

    return zona_taskuri(request)





def start_task_for_step(process_id,step):
     process = Process.objects.filter(id = process_id).first()
     flux = Flux.objects.filter(id = process.get_flux().id).first()
     deadline_days = -1;
     for assignment in Assigment.objects.all():
         if assignment.get_flux() == flux and assignment.get_step() == step:
             deadline_days = assignment.get_days()

     new_task = Task()
     for task in Task.objects.all():
         if task.get_step() == step:
             task.set_status("PENDING")
             task.set_deadline(datetime.datetime.now().date()+datetime.timedelta(days=deadline_days))
             new_task = task

     new_task.save()

     for document in Document.objects.all():
         if document.get_task().get_step() == step-1 and document.get_task().get_process() == process:
             document.set_task(new_task)
             document.save()


def add_document_to_process(request):
    document_id = request.GET.get('document_id')
    process_id = request.GET.get('procces_id')
    process1=Process.objects.filter(id=int(process_id)).first()
    document = Document.objects.filter(id = int(document_id)).first()
    tasks = Task.objects.filter(process=process1)

    for task in tasks:
        if task.get_step() == 1:
            document.set_task(task)

    document.save()

    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()
    for doc in docs:
        if doc.get_owner().username == request.user.username:
            if doc.get_status() == "FINAL":
                user_docs.append(doc)
    c["docs"] = user_docs
    c["process_id"] = process1.id

    return render(request, "process.html", c)

def start_process(request):
    process_id = int(request.GET.get('process_id'))
    start_task_for_step(process_id,1)

    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()
    for doc in docs:
        if doc.get_owner().username == request.user.username:
            if doc.get_status() == "FINAL":
                user_docs.append(doc)
    c["docs"] = user_docs
    c["process_id"] = process_id

    return render(request, "process.html", c)

def create_task_for_process(assignment_id, process_id, step):
    assignment = Assigment.objects.filter(id = assignment_id).first();
    process = Process.objects.filter(id = process_id).first();
    task = Task()
    task.set_assigment(assignment)
    task.set_process(process)
    task.set_status("NOT_STARTED")
    days = assignment.get_days()
    task.set_deadline(datetime.datetime.now().date())
    task.set_step(step)

    task.save()

    return task.id


def create_procces(request,flux_id):

    p = Process()
    p.set_starter(request.user)
    flux = Flux.objects.filter(id=int(flux_id)).first()
    p.set_flux(flux)
    p.save()

    for assignment in Assigment.objects.all():
        if assignment.get_flux().id == int(flux_id):
            create_task_for_process(assignment.id, p.id, assignment.get_step())

    return p.id


@csrf_protect
def create_file(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = CreateFileForm(request.POST)
        if form.is_valid():
            docTitle = request.POST['doctitle'].replace(" ", "")
            document = WordDocument()
            docx_title = docTitle + ".docx"
            document.add_heading(request.POST['title'], 1)
            document.add_paragraph(request.POST['text'])
            temp_path = get_project_path() + "resources\\\\0.1^" + request.user.username + docx_title
            path = get_project_path() + "resources\\\\0.1^" + request.user.username + docx_title
            print("**** " + str(path))
            document.save(temp_path)
            document_model = Document()
            document_model.set_date(timezone.now())
            document_model.set_name(docx_title)
            document_model.set_owner(request.user)
            document_model.set_path(path)
            document_model.set_status("DRAFT")
            for template in Template.objects.all():
                if template.id == 1:
                    document_model.set_template(template)
                    document_model.set_template_values(template.get_keys())
                    break
            for task in Task.objects.all():
                if task.id == 1:
                    document_model.set_task(task)
                    break
            document_model.set_type("")
            document_model.set_version(0.1)

            log = Log()
            log.set_date(datetime.datetime.now().date())
            log.set_action("CREATE DOCUMENT")
            log.set_document_name(document_model.get_name())
            log.set_document_path(document_model.get_path())
            log.set_user(document_model.get_owner())
            log.save()

            document_model.save()



            # length = f.tell()
            # f.seek(0)
            # response = HttpResponse(
            #     f.getvalue(),
            #     content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            # )
            # response['Content-Disposition'] = 'attachment; filename=' + docx_title
            # response['Content-Length'] = length
            # return response
    else:
        form = CreateFileForm()
    return render(request, "createFile.html", {'form': form})


def download_file(request):
    file_path = request.GET.get("path")
    print(">>>>>> " + str(file_path))
    fsock = open(file_path, "rb")
    doc_name = request.GET.get("doc_name")
    response = HttpResponse(fsock, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(doc_name)
    response['X-Sendfile'] = smart_str(file_path)
    return response

def edit_metadata(request):
    return render(request,"editMetadata.html")

def processes(request):
    c = {}
    c.update(csrf(request))

    fluxes = Flux.objects.all()
    c["fluxes"] = fluxes
    return render(request, "processes.html", c)

def process(request):
    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()
    for doc in docs:
        if doc.get_owner().username == request.user.username:
            if doc.get_status()=="FINAL" and doc.get_task().id==1:
                user_docs.append(doc)
    c["docs"] = user_docs
    flux_id = request.GET.get('flux_id')
    procces_id =create_procces(request,flux_id)
    c["process_id"] = procces_id
    return render(request, "process.html", c)



def zona_taskuri_initiate(request):
    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()
    print(request.user)
    for doc in docs:
        if doc.get_owner().username == request.user.username and doc.get_task().id != 1:
            user_docs.append(doc)
    c["docs"] = user_docs
    return render(request, "zona_taskuri_initiate.html", c)


def zona_taskuri(request):
    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()

    user_assigments = []
    for assigment in Assigment.objects.all():
        if assigment.get_user() != 2 and assigment.get_user().get_full_name() == request.user.username:
            user_assigments.append(assigment)

    user_tasks = []
    for assig in user_assigments:
        for task in Task.objects.all():
            if task.get_assigment() == assig and task.get_status() == "PENDING":
                user_tasks.append(task)


    for doc in Document.objects.all():
        for task in user_tasks:
            if doc.get_task() == task:
                user_docs.append(doc)

    c["docs"] = user_docs
    return render(request, "zona_taskuri.html", c)


def logs(request):
    c = {}
    c.update(csrf(request))

    user_docs = []
    docs = Document.objects.all()
    print(request.user)
    for doc in docs:
        if doc.get_owner().username == request.user.username:
            wasDeleted = deleteDocumentAfter30(request, doc)
            if wasDeleted == True:
                continue
            if doc.get_task().id == 1:
                user_docs.append(doc)
    c["docs"] = user_docs
    return render(request, "logs.html", c)
