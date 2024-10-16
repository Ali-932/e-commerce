from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.account.forms import LoginForm, RegisterForm
from ecommerce.account.models import User
from ecommerce.settings import HEAVY_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
def login_view(request):
    if request.method == 'POST':
        template = 'abstract/auth/login.html'
        sign_up_form = RegisterForm(request.POST)
        log_in_form = LoginForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            context = {
                'sign_up_form': sign_up_form,
                'log_in_form': log_in_form,
            }
            return render(request, template, context)

        if log_in_form.is_valid():
            username = log_in_form.cleaned_data['username']
            password = log_in_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'تم تسجيل الدخول بنجاح')
                return redirect('home:index')
            else:
                if User.objects.filter(username=username).exists():
                    log_in_form.add_error('password', 'كلمة المرور غير صحيحة')
                else:
                    log_in_form.add_error('username', 'اسم المستخدم غير صحيح')

            return render(request, template, {'sign_up_form': sign_up_form, 'log_in_form': log_in_form})

    if request.user.is_authenticated:
        return redirect('home:index')
    sign_up_form = RegisterForm()
    log_in_form = LoginForm()
    common = {} if request.htmx else common_views(request)

    template = 'abstract/auth/login.html'
    context = {
        'sign_up_form': sign_up_form,
        'log_in_form': log_in_form,
        **common
    }

    return render(request, template, context)

#no need for throttling
def logout_user(request):
    logout(request)
    return redirect('home:index')
