from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Customer(AbstractBaseUser):

    telegram_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    password = None


    def __str__(self):
        return self.first_name


class Category(models.Model):

    category_name = models.CharField(max_length=50, unique=True)
    category_image = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['id']


class Product(models.Model):

    Drinks = (('Sprite', 'Sprite'), ('Coca-Cola', 'Coca-Cola'), ('Fanta', 'Fanta'))
    Snacks = (('Potato Balls', 'Potato Balls'), ('French Fries', 'French Fries'), ('Country Style Potato', 'Country Style Potato'))
    kids = (('Мальчик', 'Мальчик'), ('Девочка', 'Девочка'))

    category_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    category_name = models.ForeignKey(
        Category, to_field="category_name", on_delete=models.SET_NULL, null=True, related_name="category")
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_description = models.CharField(max_length=500, blank=True)
    product_image = models.ImageField(upload_to="images/")
    Drinks = models.CharField(max_length=9, choices=Drinks, blank=True, null=True)
    Snacks = models.CharField(max_length=20, choices=Snacks, blank=True, null=True)
    Kids = models.CharField(max_length=7, choices=kids, blank=True, null=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("bbq", args=[str(self.id)])
    
    class Meta:
        ordering = ["id"]
    

class Cart(models.Model):

    customer = models.ForeignKey(Customer, to_field='telegram_id', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    product_options = models.JSONField(max_length=200, null=True)


class Order(models.Model):

    customer = models.ForeignKey(Customer, to_field='telegram_id', on_delete=models.SET_NULL, null=True)
    order_items = models.TextField()
    payment_method = models.CharField(max_length=10)
    order_address = models.CharField(max_length=250, null=True, blank=True)
    order_comment = models.CharField(max_length=500, null=True, blank=True)
    order_sum = models.IntegerField()
    order_status = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer}'s order"
    

class Comment(models.Model):

    customer = models.ForeignKey(Customer, to_field='telegram_id', on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Createad On"), auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.customer}'s comment"
    

class CustomerAddress(models.Model):

    customer = models.ForeignKey(Customer, to_field='telegram_id', on_delete=models.SET_NULL, null=True)
    address_coordinates = models.JSONField(max_length=200, null=True, blank=True)
    address_text = models.CharField(max_length=250, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        address = CustomerAddress.objects.all().filter(customer=self.customer)
        if len(address) == 5:
            first_address = CustomerAddress.objects.all().filter(customer=self.customer).first()
            first_address.delete()
        super(CustomerAddress, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer}'s addresses"
    
    class Meta:
        verbose_name_plural = "customer addresses"