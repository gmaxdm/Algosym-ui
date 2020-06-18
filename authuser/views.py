from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from authuser.forms import NewUserForm


class LoginRequired(LoginRequiredMixin):
    login_url = settings.LOGIN_URL


class RegisterView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = "auth/register.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": NewUserForm()
        })

    def form_valid(self, form):
        if self.request.method == 'POST':
            data = form.cleaned_data
            email = data['email']
            try:
                user = User.objects.get(username=email, email=email)
                messages.error(self.request,
                               "Пользователь с таким email уже зарегистрирован в системе")
            except User.DoesNotExist:
                user = User.objects.create_user(email,
                                                email=email,
                                                password=data['password2'])
                auth_login(self.request, user)
                messages.success(self.request, "Вы успешно зарегистрировались на сайте!")
                return HttpResponseRedirect(reverse("index"))
            return HttpResponseRedirect(reverse("register"))

