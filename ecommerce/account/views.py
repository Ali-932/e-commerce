from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.account.forms import LoginForm, RegisterForm


def login_view(request):
    if request.method == 'POST':
        template = 'abstract/auth/login.html'
        sign_up_form = RegisterForm(request.POST)
        log_in_form = LoginForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            context={
                'sign_up_form': sign_up_form,
                'log_in_form': log_in_form,
                'go_login': True
            }
            return render(request, template, context)

        if log_in_form.is_valid():
            user = authenticate(
                request,
                username=log_in_form.cleaned_data['username'],
                password=log_in_form.cleaned_data['password'],
            )
            messages.success(request, 'تم تسجيل الدخول بنجاح')
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home:index')
            else:
                log_in_form.add_error('username', 'اسم المستخدم أو كلمة المرور غير صحيحة')
            return render(request, template, {'sign_up_form': sign_up_form, 'log_in_form': log_in_form})

    if request.user.is_authenticated:
        return redirect('home:index')
    sign_up_form = RegisterForm()
    log_in_form = LoginForm()
    common = {} if request.htmx else common_views(request)

    template = 'abstract/auth/login.html'
    sign_up_flag = request.GET.get('sign_up', False)
    login_flag = request.GET.get('login', False)
    context = {
        'sign_up_form': sign_up_form,
        'log_in_form': log_in_form,
        'go_signup': sign_up_flag,
        'go_login': login_flag,
        **common
    }

    return render(request, template, context)

def logout_user(request):
    logout(request)
    return redirect('home:index')
