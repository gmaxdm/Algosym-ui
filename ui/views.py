from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import Algorithm, AlgoSym


_cnt = {"cnt": 0}

def default_filename():
    _cnt["cnt"] += 1
    cnt = _cnt["cnt"]
    return f"HelloWorld{cnt}.java"


def get_default_class():
    with open(settings.DEFAULT_JAVA_CLASS) as f:
        data = f.read()
        return data


@login_required
def main(request):
    try:
        algo = Algorithm.objects.get(user_id=request.user.id,
                                     pk=request.GET['id'])
    except (KeyError, Algorithm.DoesNotExist):
        try:
            algo = (Algorithm.objects.filter(user_id=request.user.id)
                                     .latest('mdate'))
        except Algorithm.DoesNotExist:
            algo = Algorithm.objects.create(user=request.user,
                                            filename=default_filename(),
                                            text=get_default_class())

    return render(request, "ui/index.html", {
        "algo": algo,
        "list": (Algorithm.objects.filter(user=request.user)
                                  .only('id', 'filename', 'mdate')
                                  .order_by('filename'))
    })


@login_required
@csrf_protect
def create(request):
    if request.method == "POST":
        algo = Algorithm.objects.create(user=request.user,
                                        filename=default_filename(),
                                        text=get_default_class())
    return HttpResponseRedirect(reverse('index'))


@login_required
@csrf_protect
def remove(request):
    if request.method == "POST":
        try:
            Algorithm.objects.filter(pk=request.POST['id']).delete()
        except KeyError:
            pass
    return HttpResponseRedirect(reverse('index'))


@login_required
@csrf_protect
def save(request):
    if request.method == "POST":
        try:
            (Algorithm.objects.filter(pk=request.POST['id'])
                              .update(text=request.POST["text"]))
        except KeyError:
            pass
    return JsonResponse({"ok": 1})


@login_required
@csrf_protect
def run(request):
    if request.method == "POST":
        try:
            algo = Algorithm.objects.get(pk=request.POST['id'])
            data = None
            with AlgoSym() as sym:
                data = sym.run(request.user, algo)
            return JsonResponse({"ok": "sent", "data": data})
        except (KeyError, Algorithm.DoesNotExist):
            pass
    return JsonResponse({"error": "algo is not defined"})


@login_required
@csrf_protect
def change_name(request):
    if request.method == "POST":
        try:
            (Algorithm.objects.filter(pk=request.POST['id'])
                              .update(filename=request.POST["name"]))
        except KeyError:
            pass
    return JsonResponse({"ok": 1})
