from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User


class PasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_("Password"),
        strip=True,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=True,
        help_text=_("Enter the same password as before, for verification.")
    )

    def clean_password2(self):
        try:
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            if password1 != password2:
                raise KeyError
        except KeyError:
            raise forms.ValidationError(
                _("Указанные пароли не совпадают!"),
                code='password_mismatch',
            )
        return password2


class NewUserForm(forms.ModelForm, PasswordForm):
    email = forms.EmailField(label=_('Email'),
                             help_text=_('Пожалуйста, введите адрес вашей электронной почты'),
                             error_messages = {'invalid': _('Адрес введен не верно!')})

    class Meta:
        model = User
        fields = ("email",)

