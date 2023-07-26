from rest_framework.viewsets import ModelViewSet
from .serializers import (CustomerSerializers, CustomerUpdateSerializers, CategorySerializers, 
                          ProductSerializers, CartSerializers, CartUpdateSerializers,
                          OrderSerializers, CommentSerializers, CustomerAddressSerializers)
from crm.models import Customer, Category, Product, Cart, Order, Comment, CustomerAddress
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.


class AllCustomersView(ModelViewSet):
    # All Customers
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers


class AllCategoriesView(ModelViewSet):
    # All Categories
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class AllProductsView(ModelViewSet):
    # All Products
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class AllCartsView(ModelViewSet):
    # All Carts
    queryset = Cart.objects.all()
    serializer_class = CartSerializers


class AllOrdersView(ModelViewSet):
    # All Orders
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class AllAddressesView(ModelViewSet):
    # All Orders
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializers


class UsersView(APIView):

    def check_user(self, request, tg_id):
        try:
            user = Customer.objects.get(telegram_id=tg_id)
        except Customer.DoesNotExist:
            return Response({"message": "Не найдено!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return user

    def get(self, request, tg_id):
        # For checking if specific user exists

        user = self.check_user(request, tg_id)
        if user:
            serializer = CustomerSerializers(user)
            return Response(serializer.data)
        return Response({"message": "Не найдено!"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, tg_id):
        # Updating user's either phone number or birthday
        
        user = self.check_user(request, tg_id)
        if user:
            serializer = CustomerUpdateSerializers(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Обновлено!"}, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors)


class CustomerAddressView(APIView):
    # Filtering addresses by telegram ID

    def get(self, request, tg_id):
        addresses = CustomerAddress.objects.filter(customer=tg_id)
        serializer = CustomerAddressSerializers(addresses, many=True)
        return Response(serializer.data)


class CategoryViewByName(APIView):
    # Checking if category under specific name exists

    def get(self, request, name):
        category_name = Category.objects.filter(category_name=name)
        serializer = CategorySerializers(category_name, many=True)
        return Response(serializer.data)


class ProductsByCategoryName(APIView):
    # Filtering products by its category name

    def get(self, request, name):
        products = Product.objects.filter(category_name=name)
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)


class ProductViewByName(APIView):
    # Checking if product under specific name exists

    def get(self, request, name):
        product = Product.objects.filter(product_name=name)
        serializer = ProductSerializers(product, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def cart_update(request, tg_id, product_id):
    # Modifying cart of a specific user

    try:
        product = Cart.objects.get(
            customer=tg_id, product_id=product_id)
    except Cart.DoesNotExist:
        return Response({"message": "Не найдено!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CartSerializers(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CartUpdateSerializers(data=request.data)
        if serializer.is_valid():
            product.product_quantity=serializer.validated_data["product_quantity"]
            product.save()
            return Response({"message": "Обновлено!"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
            product.delete()
            return Response({"message": "Удалено!"})

    return Response(status=status.HTTP_404_NOT_FOUND)


class CartByUser(APIView):
    # Accessing cart of a user

    def get(self, request, tg_id):
        cart = Cart.objects.filter(customer=tg_id)
        serializer = CartSerializers(cart, many=True)
        return Response(serializer.data)
    

    def delete(self, request, tg_id):
        cart = Cart.objects.filter(customer=tg_id)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(generics.CreateAPIView):
    # For inserting (posting) comments

    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


class Last5Orders(APIView):
    # Getting last 5 orders by a user

    def get(self, request, tg_id):
        orders = Order.objects.filter(customer=tg_id).order_by('-id')[:5]
        if orders:
            serializer = OrderSerializers(orders, many=True)
            return Response(serializer.data)
        return Response({"message": "База данных пуста!"}, status=status.HTTP_204_NO_CONTENT)


class LastOrder(APIView):
    # Getting only last order for id

    def get(self, request):
        order = Order.objects.all().order_by('-id')[:1]
        if order:
            serializer = OrderSerializers(order, many=True)
            return Response(serializer.data)
        return Response({"message": "База данных пуста!"}, status=status.HTTP_204_NO_CONTENT)

