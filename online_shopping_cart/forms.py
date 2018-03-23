from django import forms
from online_shopping_cart.models import Items
from django.core.exceptions import ValidationError


class AddItems(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('product_name', 'price', 'quantity', 'picture', 'description',)

    def clean_price(self):

        price = self.cleaned_data['price']
        try:
            float(price)
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
