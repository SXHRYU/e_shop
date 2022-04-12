from django import forms


class ContactsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.IntegerField(required=False)
    company_name = forms.CharField(label='Company Name', required=False)
    description = forms.CharField(
        label='Message',
        max_length=1000,
        required=True, 
        widget=forms.Textarea
    )
    email = forms.EmailField(max_length=100, required=True)
