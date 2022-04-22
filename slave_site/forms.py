from django import forms


class AddProductForm(forms.Form):
    label = forms.CharField()
    price = forms.IntegerField()
    url_img = forms.URLField()