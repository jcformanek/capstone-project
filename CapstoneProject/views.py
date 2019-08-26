from django.http import HttpResponseRedirect
from django.urls import reverse


def dashboard_redirect_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    elif request.user.is_staff and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('staff_dashboard'))
    return HttpResponseRedirect(reverse('postgrad_dashboard'))

