from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def authenticate(request):
    return render(request, 'authenticate.html')