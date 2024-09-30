# shop/urls.py
from django.urls import path
from . import views
from .views import product_detail, add_to_cart, remove_from_cart, update_cart, cart_detail, checkout, order_success, add_to_wishlist, remove_from_wishlist, wishlist_view, category_products

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('shop/', views.shop_page, name='shop_page'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('produktsiya/', views.produktsiya_page, name='produktsiya'),
    path('produktsiya/<slug:slug>/', views.product_page, name='product_page'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>/', product_detail, name='product_detail'),  # URL для детального просмотра продукта
    path('contact/', views.contact_page, name='contact'),  # Новый маршрут для страницы контактов
    path('category/<int:pk>/', views.category_detail, name='category_detail'),  # Используйте 'pk' вместо 'category_id'
    path('news/', views.news_list, name='news'),  # Маршрут для списка новостей
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),  # Маршрут для страницы полной новости
    path('map/', views.map_page, name='map'),  # Новый маршрут для страницы карты
    path('cart/', views.cart_detail, name='cart_detail'),
    # Cart
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order_success/', order_success, name='order_success'),
    path('products/', views.product_page, name='products_page'),
    # Wishlist
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    # Category
    path('category/<int:category_id>/', category_products, name='category_products'),
] 
