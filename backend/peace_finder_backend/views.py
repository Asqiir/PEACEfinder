from django.shortcuts import render
from django.http import HttpResponse
import datetime


def alldata(request):
    content = "Hallo Welt!"
    return HttpResponse(content, content_type='text/plain')
