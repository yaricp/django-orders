from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from .views import *

urlpatterns = patterns('',
    url(r'^$', OrdersListView.as_view(template_name='orders.html'),
        name='orders'),
    url(r'^list_type_work/$',
        TypeWorkListView.as_view(template_name='typework_list.html'),
        name='list_type_work'),
    url(r'^type_work/(?P<pk>\d+)/edit$',
        UpdateTypeWorkView.as_view(template_name='edit_type_work.html'),
        name='edit_type_work'),
    url(r'^create_type_work/$',
        CreateTypeWork.as_view(template_name="create_type_work.html"),
        name='create_type_work'),
    url(r'^create_order/$',
        CreateOrder.as_view(template_name="create_order.html"),
        name='create_order'),
    url(r'^order/(?P<pk>\d+)/$',
        OrderDetailView.as_view(template_name="order.html"),
        name='order_detail'),
    url(r'^order/(?P<pk>\d+)/comments/$',
        OrderDetailView.as_view(template_name="order_comments.html"),
        name='order_comments'),
    url(r'^order/(?P<pk>\d+)/edit$', edit_order, name='order_edit'),
    url(r'success/$',
        TemplateView.as_view(template_name="success.html"), name='success'),
)
urlpatterns += staticfiles_urlpatterns()
