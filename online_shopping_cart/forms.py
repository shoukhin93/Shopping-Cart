from django import forms
from online_shopping_cart.models import Items


class UserRegistration(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('product_name', 'price', 'quantity', 'picture', 'description',)
