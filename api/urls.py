from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductImageListView,
    ProductImageDetailView,
    CategoryListView,
    OrderView,    # Added OrderView
    ContactView   # Added ContactView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-images/', ProductImageListView.as_view(), name='product-image-list'),
    path('product-images/<int:pk>/', ProductImageDetailView.as_view(), name='product-image-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),  # New endpoint for categories
    path('orders/', OrderView.as_view(), name='order'),  # New endpoint for orders
    path('contact/', ContactView.as_view(), name='contact'),  # New endpoint for contact form
]
