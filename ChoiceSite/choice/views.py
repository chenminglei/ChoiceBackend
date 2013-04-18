from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, index!")


def detail(request):
    return HttpResponse("Hello, detail!")

def result(request):
    return HttpResponse("Hello, result!")

def vote(request):
    return HttpResponse("Hello, vote!")
