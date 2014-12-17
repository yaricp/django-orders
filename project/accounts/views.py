import json
from django.http import HttpResponseBadRequest
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response     # render, redirect,
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import Context, RequestContext     # loader,
from django.utils.translation import ugettext_lazy as _

from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         HttpResponseForbidden)
from django.views.generic import ListView, UpdateView, DetailView

from registration.backends.default.views import (
                                    RegistrationView as BaseRegistrationView)
from notifier.shortcuts import send_notification

from .models import Profile
from .forms import *


class AjaxableResponseMixin(object):

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            # Prepare JSON for parsing
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = unicode(e)
            return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            return response

    def form_valid(self, request, form):

        response = super(AjaxableResponseMixin, self).form_valid(request, form)
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps({'success': True, 'redirect_url': self.success_url}),
                mimetype="application/json"
            )
        else:
            return response


class RegistrationView(AjaxableResponseMixin, BaseRegistrationView):
    template_name = 'registration_form.html'
    success_url = '/accounts/registration_complete/'
    form_class = ProfileRegistrationForm

    def register(self, request, **kwargs):
        user = super(RegistrationView, self).register(request, **kwargs)
        del kwargs['username']
        del kwargs['password1']
        del kwargs['password2']
        #del kwargs['captcha']
        del kwargs['email']
        self.create_profile(Profile, user, **kwargs)
        admins = User.objects.filter(is_superuser=True)
        send_notification('new-user', admins)
        return

    def create_profile(self, model, user, **kwargs):
        return model.objects.get_or_create(
            user=user, defaults=kwargs
        )[0]


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            return resp_success(request, '')
        else:
            return resp_errors(request, form)
    else:
        form = PasswordChangeForm(request.user)
    c = Context({
        'form': form,
        'request': request,
        'url_form': reverse('password_change'),
        'subject_form': _(u'Changing password'),
        'submit_value': _(u'Change'),
    })
    return render_to_response('update_form.html', c,
                context_instance=RequestContext(request))


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            return resp_success(request, reverse('password_reset_done'))
        else:
            return resp_errors(request, form)
    else:
        form = PasswordResetForm()
    c = Context({
        'form': form,
        'request': request,
        'url_form': reverse('password_reset'),
        'subject_form': _(u'Reset password'),
        'submit_value': _(u'Send'),
    })
    return render_to_response('update_form.html', c,
            context_instance=RequestContext(request))


def resp_errors(request, form):
    if request.is_ajax():
    # Prepare JSON for parsing
        errors_dict = {}
        if form.errors:
            for error in form.errors:
                e = form.errors[error]
                errors_dict[error] = unicode(e)
        return HttpResponseBadRequest(json.dumps(errors_dict))
    return HttpResponseForbidden()     # catch invalid ajax and all non ajax


def resp_success(request, redirect_to):
    if request.is_ajax():
        return HttpResponse(
            json.dumps({'success': True, 'redirect_url': redirect_to}),
            mimetype="application/json"
        )
    else:
        return HttpResponseRedirect(redirect_to)


def login(request):
    if request.method == 'POST':
        request.session.set_test_cookie()
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            redirect_to = request.REQUEST.get('next')
            if redirect_to == '' or not redirect_to:
                redirect_to = reverse('profile')
            auth_login(request, form.get_user())
            return resp_success(request, redirect_to)
        else:
            return resp_errors(request, form)
    else:
        form = AuthenticationForm()
    c = Context({
        'next': request.REQUEST.get('next'),
        'form': form,
        'request': request,
    })
    return render_to_response('login_form.html', c,
            context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        pk = self.request.profile.pk
        self.kwargs.update({'pk': pk})
        object_pr = super(ProfileView, self).get_object()
        if not self.request.user.is_authenticated():
            raise Http404
        return object_pr


class UpdateProfileView(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    context_object_name = 'profile'
    fields = ['fullname', 'phone', 'info', 'address', 'pointmap', 'nikforum']

    def get_success_url(self):
        return reverse('profile')

    def get_object(self):
        pk = self.request.profile.pk
        self.kwargs.update({'pk': pk})
        object_pr = super(UpdateProfileView, self).get_object()

        if not self.request.user.is_authenticated():
            raise Http404
        return object_pr


class ManageUsersView(ListView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'manage_users.html'


class UpdateUserView(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'update_user_form.html'

    def get_success_url(self):
        return reverse('manage_users')


class DetailUserView(DetailView):
    model = Profile
    template_name = 'detail_user.html'

