from django.urls import path, include
from .views import (AllCustomersView, AllCategoriesView, AllProductsView, AllCartsView, AllOrdersView, AllAddressesView,
                    UsersView, CategoryViewByName, ProductsByCategoryName, ProductViewByName,
                    cart_update, CartByUser, CommentView, LastOrder, Last5Orders, CustomerAddressView)
from rest_framework.routers import DefaultRouter


# Registering default router for all (customers, categories, products, baskets, orders)
router = DefaultRouter()
router.register('customers', AllCustomersView)
router.register('categories', AllCategoriesView)
router.register('products', AllProductsView)
router.register('carts', AllCartsView)
router.register('orders', AllOrdersView)
router.register('addresses', AllAddressesView)



urlpatterns = [
    path('', include(router.urls)),
    path('user/<str:tg_id>/', UsersView.as_view()), # Getting user by its telegram ID or updating its phone, birthday
    path('filter/category/by-name/<str:name>/', CategoryViewByName.as_view()), # Only one category is chosen
    path('filter/products/by-category/<str:name>/', ProductsByCategoryName.as_view()), # Filtering products by its category name
    path('filter/product/by-name/<str:name>/', ProductViewByName.as_view()), # Only one product is chosen
    path('cart/<str:tg_id>/<str:product_id>/', cart_update), # Updating or Deleting products from cart of a user
    path('cart/<str:tg_id>/', CartByUser.as_view()), # Accessing a cart of a user
    path('comment/', CommentView.as_view()), # Posting a comment
    path('filter/orders/<str:tg_id>/', Last5Orders.as_view()), # Getting last 5 orders of a user
    path('last-order/', LastOrder.as_view()),# Getting last order
    path('filter/address/<str:tg_id>/', CustomerAddressView.as_view()), # Getting customer's addresses
    
]