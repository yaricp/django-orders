from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import *

urlpatterns = patterns(
    'accounts.views',
    url(r'^edit_profile/$', login_required(UpdateProfileView.as_view()),
                    name='edit_profile'),
    url(r'^manage_users/$', login_required(ManageUsersView.as_view()),
                    name='manage_users'),
    url(r'^user/(?P<pk>\d+)/edit$', login_required(UpdateUserView.as_view()),
                    name='edit_user'),
    url(r'^user/(?P<pk>\d+)/$', login_required(DetailUserView.as_view()),
                    name='detail_user'),
    url(r'^profile/$', login_required(ProfileView.as_view()),
                    name='profile'),
    url(r'^register/$', RegistrationView.as_view(),
                    name='register'),
    url(r'^registration_complete/$',
            TemplateView.as_view(template_name='registration_complete.html'),
                    name='registration_complete'),
#    url(r'^change_password/$', auth_views.change_password,
#                    name='change_password'),
    url(r'^password/change/$', password_change,
                    name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$', password_reset,
                    name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),
    url(r'^login/$', login,
                    name='auth_login'),
    url(r'^logout/$', logout,
                    name='auth_logout'),

    url(r'', include('registration.backends.default.urls')),
)
