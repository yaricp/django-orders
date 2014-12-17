# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import CaptchaField
from django.contrib.auth.forms import (
                            AuthenticationForm as BaseAuthenticationForm,
                            PasswordChangeForm as BasePasswordChangeForm,
                            PasswordResetForm as BasePasswordResetForm)
from django.utils.translation import ugettext_lazy as _


class AjaxForm(object):

    class Media:
        js = ('js/ajax_form.js', )


class UpdateUserForm(AjaxForm, ModelForm):

    class Meta(object):
        model = User
        fields = ['is_superuser', 'is_staff', 'is_active']


class AuthenticationForm(AjaxForm, BaseAuthenticationForm):

    pass


class PasswordChangeForm(AjaxForm, BasePasswordChangeForm):

    pass


class PasswordResetForm(AjaxForm, BasePasswordResetForm):

    pass


class ProfileRegistrationForm(RegistrationFormUniqueEmail):

    fullname = forms.CharField(label=_(u'fullname'))
    phone = forms.CharField(label=_(u'phone'))
    info = forms.CharField(label=_(u'additional information'),
                           required=False, widget=forms.Textarea())
    address = forms.CharField(label=_(u'address'))
    captcha = CaptchaField(label=_(u'code'))



