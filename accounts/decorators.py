from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def user_required(function=None, login_url='accounts:login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
