from rest_framework import generics, views, response
from stock_management.models import Product, ProductImage, AnimalType
from .serializers import ProductSerializer, ProductImageSerializer

# List all active products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('animal_type').prefetch_related('images')
    serializer_class = ProductSerializer

# Retrieve a single product
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('animal_type').prefetch_related('images')
    serializer_class = ProductSerializer

# List all product images
class ProductImageListView(generics.ListAPIView):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer

# Retrieve a single product image
class ProductImageDetailView(generics.RetrieveAPIView):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer

# Get all categories (both animal types and product types)
class CategoryListView(views.APIView):
    def get(self, request, *args, **kwargs):
        animal_categories = list(AnimalType.objects.values_list("name", flat=True))
        product_categories = list(Product.objects.values_list("get_product_type_display", flat=True).distinct())
        categories = list(set(animal_categories_
