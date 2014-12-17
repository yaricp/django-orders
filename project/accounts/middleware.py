from django.shortcuts import _get_queryset
from django.utils.functional import SimpleLazyObject

from .models import Profile


def get_profile(request):
    if not hasattr(request, '_cached_profile'):
        request._cached_profile = profile_for_user(request.user)
    return request._cached_profile


def profile_for_user(user):
    profile = get_object_or_none(Profile, user=user)
    if profile is not None:
        return profile


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


class UserProfileMiddleware(object):

    def process_request(self, request):
        request.profile = SimpleLazyObject(lambda: get_profile(request))
