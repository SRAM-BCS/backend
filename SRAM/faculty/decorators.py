from django.http import HttpResponseForbidden

def faculty_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user or request.user.get('auth_level') != 'admin':
            return HttpResponseForbidden('You are not authorized to access this page.')
        return view_func(request, *args, **kwargs)
    return wrapped_view