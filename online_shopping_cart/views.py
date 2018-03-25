from django.shortcuts import render, redirect
from online_shopping_cart.forms import AddItems
from online_shopping_cart.models import Items
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import collections


# Create your views here.

def index(request):
    items = Items.objects.all()
    cart_item = request.session.get('items', 0)
    return render(request, 'index.html', context={'items': items, 'cart_item': cart_item})


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
    if request.method == 'POST':
        id = request.POST['cart_item_id']

        items = request.session.get('items', [])
        items.append(id);
        print(len(items));

        request.session['items'] = items

    return HttpResponseRedirect(reverse('index'))


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


def product_summary(request):
    cart_item_ids = request.session.get('items', [])

    # Gathering duplicate elements into one place
    cleaned_cart_items = collections.Counter(cart_item_ids)
    print(cleaned_cart_items)

    cart_items = []
    total_price = 0.00
    print('cart item id', len(cart_item_ids))

    for key,value in cleaned_cart_items.items():
        temp_item = Items.objects.get(id=key)
        quantity = value
        temp_price = temp_item.price * quantity
        total_price += temp_price

        cart_items.append(
            {'product_name': temp_item.product_name, 'price': temp_item.price, 'quantity': quantity,
             'picture': temp_item.picture.url,
             'total': temp_price})

    return render(request, 'product_summary.html', context={'cart_items': cart_items, 'total_price': total_price})
