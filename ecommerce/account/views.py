from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.account.forms import LoginForm, RegisterForm
from ecommerce.account.models import User
from ecommerce.settings import HEAVY_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
def login_view(request):
    action = 'login'
    url = 'auth:login'
    if request.method == 'POST':
        template = 'abstract/auth/login.html'
        log_in_form = LoginForm(request.POST)

        if log_in_form.is_valid():
            username = log_in_form.cleaned_data['username']
            password = log_in_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'تم تسجيل الدخول بنجاح')
                return redirect('home:index')
            else:
                if User.objects.filter(username=username).exists():
                    log_in_form.add_error(error='كلمة المرور غير صحيحة', field=None)
                else:
                    log_in_form.add_error(error='اسم المستخدم غير صحيح', field=None)

            context = {
                'action': action,
                'url': url,
                'form': log_in_form
            }
            return render(request, template, context)
        else:
            context = {
                'action': action,
                'url': url,
                'form': log_in_form
            }
            return render(request, template, context)
    if request.user.is_authenticated:
        return redirect('home:index')
    log_in_form = LoginForm()
    common = {} if request.htmx else common_views(request)
    url = 'auth:login'

    template = 'abstract/auth/login.html'
    context = {
        'action': 'login',
        'url': url,
        'form': log_in_form,
        **common
    }

    return render(request, template, context)


# no need for throttling
def logout_user(request):
    logout(request)
    return redirect('home:index')


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
def register_view(request):
    url = 'auth:register'
    action = 'register'
    if request.method == 'POST':
        sign_up_form = RegisterForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            username = sign_up_form.cleaned_data['username']
            password = sign_up_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح')
            return redirect('home:index')
        if sign_up_form.errors:
            # to avoid (dictionary changed size during iteration)
            errors_copy = list(sign_up_form.errors.items())
            for field, errors in errors_copy:
                if field == '__all__':
                    continue
                sign_up_form.add_error(error=errors[0], field=None)
        context = {
            'action': action,
            'url': url,
            'form': sign_up_form
        }
        return render(request, 'abstract/auth/login.html', context)

    if request.user.is_authenticated:
        return redirect('home:index')
    sign_up_form = RegisterForm()
    common = {} if request.htmx else common_views(request)

    template = 'abstract/auth/login.html'
    context = {
        'action': action,
        'url': url,
        'form': sign_up_form,
        **common
    }

    return render(request, template, context)
