from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect

from products.models import Product
from products.forms import ProductModelForm

# Create your views here.
def search_view(request, *args, **kwargs):
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    context = {"name": "*your name*", "query": query}
    return render(request, "home.html", context)

@staff_member_required
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = ProductModelForm()
    return render(request, "forms.html", {"form": form})
    
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
