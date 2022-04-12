from django.forms import ModelForm
from .models import Product
# from .countries import Countries


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class SearchForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'maker', 
            'category', 
            # 'country_of_origin'
        ]


# Such forms are used for everything, EXCEPT interacting with database
#     title       = forms.CharField(label='Title', max_length=100)
#     description = forms.CharField(label='<h2>Description</h2>', required=False)
#     category    = forms.CharField(max_length=100)
#     maker       = forms.CharField(max_length=100)
#     price       = forms.DecimalField(max_digits=20, decimal_places=2)
#     country_of_origin = forms.ChoiceField(required=False, choices=Countries.country_codes)
#     # country_of_origin = forms.ChoiceField(required=False, choices=[('US', 'USA'), ('RU', 'RUS')], initial='US')

# print(dir(AddProductForm))