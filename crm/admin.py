from django.contrib import admin
from .models import Customer, Category, Product, Order, Comment
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    # Customized Customer model in admin panel
    list_display = ("first_name", "username", "phone_number", "registered_at", "view_orders_link")
    list_filter = ("registered_at", )

    def view_orders_link(self, obj):
        count = obj.order_set.count()
        url = (
            reverse("admin:crm_order_changelist") + "?" +
            urlencode({"customers__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} order(s)</a>', url, count)

    view_orders_link.short_description = "Orders"


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


class ProductAdmin(admin.ModelAdmin):
    # Customized Product model in admin panel

    list_display = ("product_name", "category_name", "product_price",)
    list_filter = ("category_name",)
    search_fields = ("name__startswith",)


class OrderAdmin(admin.ModelAdmin):
    # Customized Order model in admin panel

    list_display = ("customer", "items", "payment_method", "sum", "status", "created_at", "is_paid", "is_refunded")
    list_filter = ("created_at", "sum", "status", "payment_method", "is_refunded")


class CommentAdmin(admin.ModelAdmin):
    # Customized Comment model in admin panel

    list_display = ("customer", "comment", "created_at")


admin.site.unregister(Group)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
