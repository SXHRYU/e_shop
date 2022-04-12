from django.contrib import admin
from .models import Maker, Category, Product

# Register your models here.
admin.site.register(Maker)
admin.site.register(Category)
admin.site.register(Product)