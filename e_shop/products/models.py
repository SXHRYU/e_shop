from django.db import models
from .countries import Countries
from django.urls import reverse
from django.core.validators import MinValueValidator


# My models go here
# Maker, as in the manufacturer of the Product.
class Maker(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=322, blank=True)

    class Meta:
        verbose_name_plural = "makers"

    def get_absolute_url(self):
        return reverse("products-maker", kwargs={"id_": self.id})

    def __str__(self) -> str:
        return self.name
    

# Category of Product, like TV, PC, laptop, phones, etc.
class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    # !!! TO DO !!!
    # Actually come up with some idea for main page for categories.
    # def get_absolute_url(self):
    #     return reverse("category_detail", kwargs={"pk": self.pk})
    


# The product itself.
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    # References 'Category' model
    category = models.ForeignKey(
        # What model does the Product references.
        Category,
        # NULL is set on all products when the parent Category is deleted.
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    maker = models.ForeignKey(
        Maker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(
            limit_value=0, 
            message='Price cannot be negative!'
        )]
    )
    country_of_origin = models.CharField(
        max_length=2, 
        choices=Countries.country_codes, 
        default='US',
        blank=True)
    
    class Meta:
        verbose_name_plural = "products"

    def get_absolute_url(self):
        return reverse('products-detail', kwargs={'id_' : self.id})

    def __str__(self) -> str:
        return self.title
