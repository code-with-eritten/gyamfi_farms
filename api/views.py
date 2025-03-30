from rest_framework import generics
from stock_management.models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer

# List all products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).prefetch_related('images')
    serializer_class = ProductSerializer

# Retrieve a single product
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).prefetch_related('images')
    serializer_class = ProductSerializer

# List all product images
class ProductImageListView(generics.ListAPIView):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer

# Retrieve a single product image
class ProductImageDetailView(generics.RetrieveAPIView):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer
