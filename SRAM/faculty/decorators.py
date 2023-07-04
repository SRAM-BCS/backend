from django.http import HttpResponseForbidden
from SRAM.constants import AUTHORIZATION_LEVELS
def faculty_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.token or request.token.get('authorizationLevel') < AUTHORIZATION_LEVELS['FACULTY']:
            return HttpResponseForbidden('You are not authorized to access this page.')
        return view_func(request, *args, **kwargs)
    return wrapped_view