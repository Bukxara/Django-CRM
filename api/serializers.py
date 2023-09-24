from rest_framework import serializers
from crm.models import Customer, Category, Product, Cart, Order, Comment, CustomerAddress, ProductOptionPrice


class CustomerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('first_name', 'username', 'telegram_id', 'phone_number')


class CustomerUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('phone_number', 'birthday')


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_image')


class ProductOptionPriceSerializers(serializers.ModelSerializer):
    option_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductOptionPrice
        fields = ('product', 'option_name', 'option_price')
    
    def get_option_name(self, instance):
        return instance.option.name


class ProductSerializers(serializers.ModelSerializer):
    product_options = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_price', 'product_description', 'product_image', 'has_different_options', 'product_options')
    
    def get_product_options(self, instance):
        product_options = instance.productoptionprice_set.all()
        return ProductOptionPriceSerializers(product_options, many=True).data


class CartSerializers(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('customer', 'product_id', 'product_quantity', 'product_options')


class CartUpdateSerializers(serializers.Serializer):

    product_quantity = serializers.IntegerField()
    product_options = serializers.CharField(required=False)


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'customer', 'items', 'payment_method', 'address', 'comment', 'sum', 'status')


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('customer', 'comment')


class CustomerAddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomerAddress
        fields = ('customer', 'address_coordinates', 'address_text')