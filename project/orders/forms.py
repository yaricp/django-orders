# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Q

from django import forms
from django.forms import ModelForm


from .models import Order
from .widgets import TimePickerWidget


class OrderForm(ModelForm):

    class Media:
        js = ('js/ajax_form.js', )

    class Meta(object):
        model = Order
        widgets = {
            'time_work': TimePickerWidget(params="showOn: 'button', "
                                "buttonImage: '/static/images/icon_clock.gif',"
                                "buttonImageOnly: true",
                                attrs={'class': 'timepicker', }), }


class CreateOrderForm(OrderForm):

    description = forms.CharField(widget=forms.Textarea)

    class Meta(OrderForm.Meta):
        fields = ['type_work', 'time_work', 'description']


class ClientOrderEditForm(OrderForm):

    STATUS = (  (0, _(u'init')),
                (4, _(u'cancel')),)
    status = forms.ChoiceField(widget=forms.Select(), choices=STATUS)
    description = forms.CharField(widget=forms.Textarea)

    class Meta(OrderForm.Meta):
        fields = ['type_work', 'time_work', 'description', 'status', 'progress']


class BossOrderEditForm(OrderForm):

    STATUS = (
        (1, _(u'start')),
        (2, _(u'end')),
        (3, _(u'wait')),
        (4, _(u'cancel')),

        )
    status = forms.ChoiceField(widget=forms.Select(), choices=STATUS)

    class Meta(OrderForm.Meta):
        fields = ['status', 'summa', 'time_work', 'worker', 'paid']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['worker'].queryset = User.objects.filter(
                                              Q(is_staff=True) |
                                              Q(is_superuser=True))


class ManagerOrderEditForm(OrderForm):

    STATUS = (
        (2, _(u'end')),
        (3, _(u'wait')),
        (4, _(u'cancel')),
        )
    status = forms.ChoiceField(widget=forms.Select(), choices=STATUS)

    class Meta(OrderForm.Meta):
        fields = ['status', 'summa', 'time_work', 'paid']


class ManagerFirstOrderEditForm(OrderForm):

    class Meta(OrderForm.Meta):
        fields = ['summa', 'paid']


