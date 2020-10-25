from django import forms
from customers.models import Customer, Address

delivery_choices = [('pickup','pickup'),
                    ('delivery','delivery'),]

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name *'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name *'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email *'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    # delivery = forms.BooleanField(required=False)
    # pickup = forms.BooleanField(required=False)

    street_one = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Address Line 1 *'}))
    street_two = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Address Line 2 *'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City *'}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'State *'}))
    zipcode = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Zipcode *'}))
