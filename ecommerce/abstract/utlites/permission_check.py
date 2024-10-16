
from django.shortcuts import redirect
from django.contrib import messages
def permission_check(request):
    messages.error(request, 'يجب تسجيل الدخول اولا')
    return (None, None) if request.htmx else redirect('home:index')
