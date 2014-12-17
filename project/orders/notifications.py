__author__ = 'yaric'

from django.contrib.auth.models import User
from notifier.shortcuts import create_notification, update_preferences

#notifications
create_notification('new-order')
create_notification('staff-change-order-status')
create_notification('user-change-order-status')

#Users fo notifications
users = User.objects.filter(is_superuser=False, is_staff=False)
staffs = User.objects.filter(is_staff=True)
for user in staffs:
    update_preferences('new-order', user, {'email': True})
    update_preferences('user-change-order-status', user, {'email': True})
for user in users:
    update_preferences('staff-change-order-status', user, {'email': True})