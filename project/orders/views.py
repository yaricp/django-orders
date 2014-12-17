# Create your views here.
import json
from time import localtime, strftime
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from notifier.shortcuts import send_notification

from .models import TypeWork, Order
from .forms import *


class TypeWorkListView(ListView):

    model = TypeWork
    context_object_name = 'works'


class CreateTypeWork(CreateView):

    model = TypeWork

    def get_success_url(self):
            return reverse('list_type_work')


class UpdateTypeWorkView(UpdateView):
    model = TypeWork

    def get_success_url(self):
            return reverse('list_type_work')


class OrdersListView(ListView):

    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        ''' '''
        curr_user = self.request.user
        if curr_user.is_authenticated():
            if not (curr_user.is_staff or curr_user.is_superuser):
                qs = Order.objects.filter(client=curr_user)
            else:
                qs = Order.objects.all()
        else:
            qs = None
        return qs


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order.html'


class UpdateOrder(UpdateView):

    model = Order
    form_class = ClientOrderEditForm
    template_name = 'order_edit.html'

    def get_success_url(self):
            return reverse('orders')

    def form_invalid(self, form):
        response = super(UpdateOrder, self).form_invalid(form)
        if self.request.is_ajax():
            # Prepare JSON for parsing
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = unicode(e)
            return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            pass
        return response

    def form_valid(self, form):
        order = form.save(commit=False)

        if self.__class__.__name__ == 'ManagerFirstUpdateOrder':

            order.worker = self.request.user
            order.status = 1
            notific_context = {
            'mess': _(u'Your order was start in our system. Manager '\
                        + order.worker.username + \
                      'will work with your order. thank you'),
            'order': order,
        }
            send_notification('staff-change-order-status',
                                order.client, context=notific_context)
        elif self.__class__.__name__ == 'ManagerUpdateOrder':
            order.worker = self.request.user
            notific_context = {
            'mess': _(u'Status of your order was changed on'
                        + order.get_status_display() + '. Thank you.'),
            'order': order,
        }
            send_notification('staff-change-order-status',
                                order.client, context=notific_context)
        elif self.__class__.__name__ == 'ClientUpdateOrder':
            notific_context = {
            'mess': _(u'Status of order ' + order.get_absolute_url()\
            + ' was changed by ' + order.client.username + '. Thank you.'),
            'order': order,
        }
            send_notification('user-change-order-status', order.worker,
                                                context=notific_context)
        order.save()
        response = super(UpdateOrder, self).form_valid(form)
        if self.request.is_ajax():
            return HttpResponse(
                        json.dumps({'success': True, 'redirect_url': ''}),
                        mimetype="application/json"
                    )
        else:
            pass
        return response


class CreateOrder(CreateView):
    model = Order
    form_class = CreateOrderForm

    def get_success_url(self):
            return reverse('orders')

    def form_invalid(self, form):
        response = super(CreateOrder, self).form_invalid(form)
        if self.request.is_ajax():
            # Prepare JSON for parsing
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = unicode(e)
            return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            pass
        return response

    def form_valid(self, form):
        order = form.save(commit=False)
        default_worker = User.objects.get(pk=1)
        order.client = self.request.user
        order.status = 0
        order.timestart = strftime("%Y-%m-%d %H:%M:%S", localtime())
        order.progress = 0
        order.worker = default_worker
        order.save()
        response = super(CreateOrder, self).form_valid(form)
        notific_context = {
            'mess': _(u'Is new order in system. ' + order.client.username\
                     + ' want to make ' + order.type_work.name\
                      + ' - ' + str(order.time_work) + ' hours.'),
            'order': order,
        }
        staffs = User.objects.filter(is_staff=True)
        send_notification('new-order', staffs, context=notific_context)

        if self.request.is_ajax():
            return HttpResponse(
                        json.dumps({'success': True, 'redirect_url': ''}),
                        mimetype="application/json"
                    )
        else:
            pass
        return response


class BossUpdateOrder(UpdateOrder):

    form_class = BossOrderEditForm


class ManagerUpdateOrder(UpdateOrder):

    form_class = ManagerOrderEditForm


class ManagerFirstUpdateOrder(UpdateOrder):

    form_class = ManagerFirstOrderEditForm


class ClientUpdateOrder(UpdateOrder):

    form_class = ClientOrderEditForm


order_edit_form_client = ClientUpdateOrder.as_view()
order_edit_form_boss = BossUpdateOrder.as_view()
order_edit_form_manager = ManagerUpdateOrder.as_view()
order_edit_form_manager_first = ManagerFirstUpdateOrder.as_view()


def edit_order(request, pk):
    user = request.user
    if user.is_authenticated():
        if user.is_superuser:
            #print 1
            return order_edit_form_boss(request, pk=pk)
        elif user.is_staff:
            #print 2
            if Order.objects.get(pk=pk).status == 0:
                #print 3
                return order_edit_form_manager_first(request, pk=pk)
            else:
                #print 4
                return order_edit_form_manager(request, pk=pk)
        else:
            #print 5
            return order_edit_form_client(request, pk=pk)

