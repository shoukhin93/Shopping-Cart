from django import forms
from online_shopping_cart.models import Items, Information
from django.core.exceptions import ValidationError
import math


class AddItems(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('product_name', 'price', 'quantity', 'picture', 'description',)

    def clean_price(self):

        price = self.cleaned_data['price']
        try:

            price = float(price)
            price = (math.ceil(price * 100) / 100)  # Rounding into 2 floating points
        except ValueError:
            raise ValidationError("Invalid Price")

        return price

    def clean_quantity(self):

        quantity = self.cleaned_data['quantity']
        try:
            int(quantity)
        except ValueError:
            raise ValidationError("Invalid Quantity")

        return quantity


class AddShipplingInfo(forms.ModelForm):
    class Meta:
        model = Information
        fields = ('first_name', 'last_name', 'email', 'contact_no', 'full_address', 'zipcode',)
