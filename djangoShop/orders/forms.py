from django import forms


class CreateOrderForm(forms.Form):

    choices = [
        ("0", "False"),
        ("1", "True"),
    ]

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=choices)
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=choices)
