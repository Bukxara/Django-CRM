from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class AbstractBaseModel(models.Model):
    # Abstract Class for other models

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(AbstractBaseModel, AbstractBaseUser):
    # Customer model for Users that inherits from AbstractBaseUser

    telegram_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    password = None
    last_login = None

    USERNAME_FIELD = 'telegram_id'

    def number_of_orders(self):
        # Displays number of orders initiated by a customer

        count = Order.objects.filter(customer=self.telegram_id).count()
        return count

    number_of_orders.short_description = "Orders"

    def last_order(self):
        # Last order of a customer

        last_order = Order.objects.filter(customer=self.telegram_id).last()
        return last_order

    def __str__(self):
        return self.first_name


class AbstractCustomerModel(models.Model):
    # Abstract Class defining author (customer)

    customer = models.ForeignKey(
        Customer, to_field='telegram_id', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Category(AbstractBaseModel):

    category_name = models.CharField(max_length=50, unique=True)
    category_image = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['id']


class Product(AbstractBaseModel):
    # Model for all the available products

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)

    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField(blank=True, null=True)
    product_description = models.CharField(max_length=500, blank=True)
    product_image = models.ImageField(upload_to="images/")
    has_different_options = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("bbq", args=[str(self.id)])

    class Meta:
        ordering = ["id"]
        

class ProductOption(AbstractBaseModel):

    name = models.CharField(max_length=255, help_text='Mahsulotga tegishli bo\'lgan qo\'shimcha opsiya nomi')

    def __str__(self):
        return self.name


class ProductOptionPrice(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    option_price = models.IntegerField()

    def __str__(self):
        return f"{self.product}'s option"
    
    
class Cart(AbstractCustomerModel):
    # Model for storing different customers' carts (of products)

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    product_options = models.JSONField(max_length=200, null=True)


class Order(AbstractBaseModel, AbstractCustomerModel):
    # Model for orders initiated by customers

    statuses = (("Kutmoqda", "Kutmoqda"), ("Pishirilmoqda", "Pishirilmoqda"), ("Yetkazilmoqda", "Yetkazilmoqda"),
                ("Yetkazilgan", "Yetkazilgan"), ("Bekor qilingan", "Bekor qilingan"))

    payment_methods = (("Karta", "Karta"), ("Naqd", "Naqd"))

    items = models.TextField()
    payment_method = models.CharField(choices=payment_methods, max_length=5)
    address = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)
    sum = models.IntegerField()
    status = models.CharField(
        choices=statuses, default="Pending", max_length=14)
    is_paid = models.BooleanField(_("Paid"), default=False)
    is_refunded = models.BooleanField(_("Refunded"), default=False)

    def __str__(self):
        return f"{self.customer}ning buyurtmasi"

    @property
    def is_paid_online(self):
        # Whether order is paid online or not
        return self.payment_method in ("Karta")

    def change_status(self, new_status):
        # Changes the status of the order

        if new_status not in (status[0] for status in self.statuses):
            raise ValueError("Bunday status mavjud emas!")
        if self.is_paid_online:
            if new_status == "Pishirilmoqda":
                self.is_paid = True
            elif self.status in ("Pishirilmoqda", "Yetkazilmoqda") and new_status == "Bekor qilingan":
                self.is_refunded = True
        else:
            if new_status == "Yetkazilgan":
                self.is_paid = True
        self.status = new_status
        self.save()


class Comment(AbstractBaseModel, AbstractCustomerModel):

    comment = models.TextField()

    def __str__(self):
        return f"{self.customer}'s comment"


class CustomerAddress(AbstractCustomerModel):

    address_coordinates = models.JSONField(
        max_length=255, null=True, blank=True)
    address_text = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        addresses = CustomerAddress.objects.all().filter(customer=self.customer)
        if len(addresses) == 5:
            first_address = CustomerAddress.objects.all().filter(
                customer=self.customer).first()
            first_address.delete()
        super(CustomerAddress, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer}ning adreslari"

    class Meta:
        verbose_name_plural = "customer addresses"


