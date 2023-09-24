from django.contrib import admin
from django import forms
from .models import Customer, Category, Product, Order, Comment, ProductOption, ProductOptionPrice
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    # Customized Customer model in admin panel
    list_display = ("first_name", "username",
                    "phone_number", "registered_at", )
    list_filter = ("registered_at", )


class CategoryAdmin(admin.ModelAdmin):
    # Customized Category model in admin panel

    list_display = ("category_name", "view_products_link")

    def view_products_link(self, obj):
        count = obj.product_set.count()
        url = (
            reverse("admin:crm_product_changelist") + "?" +
            urlencode({"categories__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Products</a>', url, count)

    view_products_link.short_description = "Products"


class ProductOptionPriceInline(admin.TabularInline):
    model = ProductOptionPrice
    extra = 1


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.has_different_options:
            # If has_different_options is True, include the option_name and option_price fields
            self.fields['option_name'] = forms.CharField(label='Option Name')
            self.fields['option_price'] = forms.DecimalField(
                label='Option Price')


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductOptionPriceInline]
    list_display = ('product_name', 'category', 'product_description', 'has_different_options',)
    form = ProductAdminForm
    fieldsets = (
        (None, {
            'fields': ('category', 'product_name', 'product_description', 'product_image', 'has_different_options', 'product_price',)
        }),
    )


class ProductOptionAdmin(admin.ModelAdmin):
    # Customized ProductOption model in admin panel

    list_display = ("name", )
    search_fields = ("name_contains", )


class ProductOptionPriceAdmin(admin.ModelAdmin):
    # Customized ProductOption model in admin panel

    list_display = ('product', 'option', 'option_price')
    search_fields = ("product_contains", )


class OrderAdmin(admin.ModelAdmin):
    # Customized Order model in admin panel

    list_display = ("customer", "items", "payment_method", "sum",
                    "status", "created_at", "is_paid", "is_refunded")
    list_filter = ("created_at", "sum", "status",
                   "payment_method", "is_refunded")


class CommentAdmin(admin.ModelAdmin):
    # Customized Comment model in admin panel

    list_display = ("customer", "comment", "created_at")


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
admin.site.register(ProductOptionPrice, ProductOptionPriceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
