__author__ = 'yaric'

from django.contrib.auth.models import User
from notifier.shortcuts import create_notification, update_preferences

create_notification('new-user')
admins = User.objects.filter(is_superuser=True)
for adm in admins:
    update_preferences('new-user', adm, {'email': True})