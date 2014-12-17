from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^orders/', include('project.orders.urls')),
    #url(r'^accounts/profile/', TemplateView.as_view(template_name="profile.html"), name='profile'),
    url(r'^accounts/', include('project.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^contacts/', TemplateView.as_view(template_name="contacts.html"), name='contacts'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
urlpatterns += staticfiles_urlpatterns()
