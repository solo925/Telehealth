from django import forms


class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    amount = forms.IntegerField()
