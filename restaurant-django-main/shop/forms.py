# forms.py
from django import forms

class RatingForm(forms.Form):
    score = forms.ChoiceField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])

# shop/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'subcategory', 'price', 'desc', 'pub_date', 'image']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive whole number.")
        return price

    def clean_desc(self):
        desc = self.cleaned_data.get('desc')
        if not desc:
            raise forms.ValidationError("Description is required.")
        return desc

    def clean_pub_date(self):
        pub_date = self.cleaned_data.get('pub_date')
        if not pub_date:
            raise forms.ValidationError("Enter a valid date.")
        return pub_date
