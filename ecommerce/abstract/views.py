from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
# Create your views here.


def beenLimited(request, exception):
    messages.error(request, 'لقد تم تجاوز الحد الاقصى للطلبات')
    raise exception
