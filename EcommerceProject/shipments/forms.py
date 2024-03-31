from paypal.standard.forms import PayPalPaymentsForm
from django import forms
from .models import ShippingAddress
class CustomPayPalPaymentsForm(PayPalPaymentsForm):

    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""
class AddressForm(forms.ModelForm):
    class Meta:
        model=ShippingAddress
        fields=['first_name','last_name','email','phone','region','city_or_district','neighborhood','street','post_code','home_number']