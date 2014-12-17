#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class TypeWork(models.Model):

    name = models.CharField(verbose_name=_(u'Name'), max_length=100)

    def __unicode__(self):
        return self.name


class Order(models.Model):

    STATUS = (
        (0, _(u'init')),
        (1, _(u'start')),
        (2, _(u'end')),
        (3, _('wait')),
        (4, _('cancel')),
        )


    client = models.ForeignKey(User, verbose_name=_(u'Client'),
                                                        related_name='clients')
    timestart = models.DateTimeField(verbose_name=_(u'date of initialization'))
    type_work = models.ForeignKey(TypeWork, verbose_name=_(u'type of work'))
    time_work = models.TimeField(verbose_name=_(u'time of work prev'))
    status = models.IntegerField(verbose_name=_(u'status of order'),
                            max_length=1, choices=STATUS, default=0, null=True)
    worker = models.ForeignKey(User, verbose_name=_(u'Worker'),
                                        related_name='workers')
    summa = models.DecimalField(verbose_name=_(u'Sum'), max_digits=9,
                                                    decimal_places=2, null=True)
    progress = models.IntegerField(verbose_name=_(u'Progress'))
    description = models.CharField(verbose_name=_(u'Description'),
                                                        max_length=300)
    paid = models.BooleanField(verbose_name=_(u'status of pay'), default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('order_detail', (), {'pk': self.pk})


