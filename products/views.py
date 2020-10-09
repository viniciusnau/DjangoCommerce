from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from products.models import Product

# Create your views here.
def search_view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    context = {"name": "*your name*", "query": query}
    return render(request, "home.html", context)

def product_create_view(request, *args, **kwargs):
    return render(request, "forms.html", context)

def product_detail_view(request, pk):
    try:
        obj = Product.objects.get(pk= pk)
    except Product.DoesNotExist:
        raise Http404
    return render(request, "products/detail.html", {"object": obj})

def product_api_detail_view(request, pk, *args, **kwargs):
    try:
        obj = Product.objects.get(pk= pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Page Not Found"})
    return JsonResponse({"id": obj.id})

def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/list.html", context)
