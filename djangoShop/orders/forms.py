import re
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

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]

        if not data.isdigit():
            raise forms.ValidationError("Phone number should have only numbers")

        pattern = re.compile(r"^\d{10}$")
        if not pattern.match(data):
            raise forms.ValidationError("Phone number wrong format")

        return data
