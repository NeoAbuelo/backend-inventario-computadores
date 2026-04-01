from django.shortcuts import render


def index(request):
    return render(request, 'doc/index.html')


def inventario(request):
    return render(request, 'doc/inventario.html')


def salapcs(request):
    return render(request, 'doc/salapcs.html')
