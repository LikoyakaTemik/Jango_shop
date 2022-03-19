from django.shortcuts import render

def get_base_context(request):
    menu = [
        {"link": "/catalog/", "text": "Каталог"},
    ]

    return {"menu": menu, "user": request.user}

def index_page(request):
    context = get_base_context(request)
    return render(request, "index.html", context)

def catalog_page(request):
    context = get_base_context(request)
    return render(request, "catalog.html", context)

def login_page(request):
    context = get_base_context(request)
    return render(request, "login.html", context)
