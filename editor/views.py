from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the editor index.")

def show_path(request, path):
    return HttpResponse(f'Your path is {path}')