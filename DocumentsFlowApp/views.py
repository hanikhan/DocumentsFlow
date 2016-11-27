from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect


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
