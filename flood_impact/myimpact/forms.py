from django import forms


class AddressForm(forms.Form):
    address = forms.CharField(label="Address", max_length=65)
