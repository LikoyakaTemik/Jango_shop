from django import forms
from django.forms import ModelForm


class AddProductForm(forms.Form):
    label = forms.CharField()
    price = forms.IntegerField()
    url_img = forms.URLField()

class AddToCartForm(forms.Form):
    username = forms.CharField()

class CreateChatForm(forms.Form):
    username = forms.CharField()

class ChatInputForm(forms.Form):
    mes = forms.CharField()

class ChatOutputForm(forms.Form):
    username = forms.CharField()