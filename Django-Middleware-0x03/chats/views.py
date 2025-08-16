from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def chat_view(request):
    return HttpResponse("Welcome to the chat!")
