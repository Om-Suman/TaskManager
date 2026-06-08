from django import http
from django.contrib import admin

# Register your models here.
def members(request):
    return http.Response("Hello World")