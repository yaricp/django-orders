from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):

    user = models.OneToOneField(User, verbose_name=_(u'user'),
                                related_name='%(class)s')

    fullname = models.CharField(_(u'fullname'), max_length=100)
    phone = models.CharField(_(u'phone number'), max_length=100)
    info = models.TextField(_(u'additional information'), blank=True)
    address = models.CharField(_(u'address'), max_length=255)
    pointmap = models.URLField(null=True)
    nikforum = models.URLField(null=True)

    def __unicode__(self):
        return self.fullname

#class PointMap(models.Model):
    #
    #def __init__(self):
        #super(PointMap, self).__init__()

    #profile = models.ForeingKey(Profile)
    #link = models.CharField(_(u'address'), max_length=255)