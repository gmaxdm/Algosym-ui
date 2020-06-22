import logging

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import Algorithm, AlgoSym


logger = logging.getLogger(__name__)


DEFAULT_CLASSNAME = "HelloWorld"


def get_default_class():
    with open(settings.DEFAULT_JAVA_CLASS) as f:
        data = f.read()
        return data


@login_required
def main(request):
    algos_qs = (Algorithm.objects.filter(user=request.user)
                                 .only('id', 'filename', 'mdate')
                                 .order_by('filename'))
    try:
        algo = Algorithm.objects.get(user_id=request.user.id,
                                     pk=request.GET['id'])
    except (KeyError, Algorithm.DoesNotExist):
        try:
            algo = (Algorithm.objects.filter(user_id=request.user.id)
                                     .latest('mdate'))
        except Algorithm.DoesNotExist:
            algo = Algorithm.objects.create(user=request.user,
                                            filename="{}{}.java".format(DEFAULT_CLASSNAME,
                                                                        algos_qs.count()),
                                            text=get_default_class())

    return render(request, "ui/index.html", {
        "algo": algo,
        "list": algos_qs
    })


@login_required
@csrf_protect
def create(request):
    if request.method == "POST":
        algo = Algorithm.objects.create(user=request.user,
                                        filename="{}{}.java".format(DEFAULT_CLASSNAME,
                                                                    (Algorithm.objects
                                                                              .filter(user=request.user)
                                                                              .count())),
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
            action = request.POST.get('action', 'run')
            algo = Algorithm.objects.get(pk=request.POST['id'])
            data = None
            with AlgoSym() as sym:
                if action == "run":
                    data = sym.run(request.user, algo)
                    if data and "id" in data:
                        algo.run_id = data["id"]
                        algo.status = data["info"]
                elif action == "status":
                    data = sym.status(request.user, algo)
                    if data and "status" in data:
                        algo.metrics = data["metrics"] or ""
                        algo.status = data["status"]
                if data:
                    algo.save()
            return JsonResponse({"data": data})
        except (KeyError, Algorithm.DoesNotExist) as err:
            logger.exception(err)
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
