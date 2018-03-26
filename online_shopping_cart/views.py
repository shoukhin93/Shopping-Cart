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


def edit_item(request, id):
    """ To Edit Item from database(Admin privilege required)"""
    item = Items.objects.get(id=id)

    if request.method == "POST":
        updated_info = AddItems(request.POST, request.FILES)

        if updated_info.is_valid():
            AddItems(request.POST, request.FILES, instance=item).save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'edit_item.html', context={'item': item})


def delete_item(request, id):
    """ To Delete Item from database(Admin privilege required)"""
    Items.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('index'))


def product_summary(request):
    """To view the cart items which are stored in session"""

    cart_item_ids = request.session.get('items', [])

    # Gathering duplicate elements into key, occurrences  pair
    cleaned_cart_items = collections.Counter(cart_item_ids)

    cart_items = []
    total_price = 0.00

    for key, value in cleaned_cart_items.items():
        # Getting the saved item from database
        temp_item = Items.objects.get(id=key)

        quantity = value
        temp_price = temp_item.price * quantity  # total Price of a single item = quantity * price
        total_price += temp_price  # Total shopping price

        cart_items.append(
            {'id': key, 'product_name': temp_item.product_name, 'price': temp_item.price, 'quantity': quantity,
             'picture': temp_item.picture.url,
             'total': temp_price})

    return render(request, 'product_summary.html', context={'cart_items': cart_items, 'total_price': total_price})


def add_cart_item(request):
    """To add cart item and save to session"""
    if request.method == 'POST':
        id = int(request.POST['cart_item_id'])
        items = request.session.get('items', [])
        items.append(id);

        request.session['items'] = items

    return HttpResponseRedirect(reverse('index'))


def remove_cart_item(request, id):
    """To remove cart item from session"""

    updated_cart_items = request.session.get('items', [])
    updated_cart_items = [x for x in updated_cart_items if x != id]

    request.session['items'] = updated_cart_items

    return HttpResponseRedirect(reverse('product_summary'))
