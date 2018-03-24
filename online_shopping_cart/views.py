from django.shortcuts import render, redirect
from online_shopping_cart.forms import AddItems
from online_shopping_cart.models import Items
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def index(request):
    items = Items.objects.all()
    return render(request, 'index.html', context={'items': items})


def admin_panel(request):
    if request.method == 'POST':
        form = AddItems(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPanel')
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('adminPanel'))

    return render(request, 'admin_panel.html')


def test(request):
    items = Items.objects.all()
    return render(request, 'test.html', context={'items': items})


def edit_item(request, id):
    item = Items.objects.get(id=id)

    if request.method == "POST":
        updated_info = AddItems(request.POST, request.FILES)

        if updated_info.is_valid():
            AddItems(request.POST, request.FILES, instance=item).save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'edit_item.html', context={'item': item})


def delete_item(request, id):
    Items.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('index'))
