from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductImageListView,
    ProductImageDetailView,
    CategoryListView  # Added category view
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-images/', ProductImageListView.as_view(), name='product-image-list'),
    path('product-images/<int:pk>/', ProductImageDetailView.as_view(), name='product-image-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),  # New endpoint for categories
]
