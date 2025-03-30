from rest_framework import generics, views
from rest_framework.response import Response
from django.http import JsonResponse
from django.middleware import common
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache  # Correct import
from stock_management.models import Product, ProductImage, AnimalType
from .serializers import ProductSerializer, ProductImageSerializer


# Enable CORS Headers for All Origins
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')  # Corrected no_cache to never_cache
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('animal_type').prefetch_related('images')
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('animal_type').prefetch_related('images')
    serializer_class = ProductSerializer


class ProductImageListView(generics.ListAPIView):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer


class ProductImageDetailView(generics.RetrieveAPIView):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer


class CategoryListView(views.APIView):
    """Fetches a combined list of all categories (Animal Types + Product Types)"""
    
    def get(self, request, *args, **kwargs):
        animal_categories = list(AnimalType.objects.values_list('name', flat=True))  # ['Poultry', 'Goat', ...]
        product_categories = list(Product.objects.values_list('product_type', flat=True).distinct())  # ['EGG', 'MEAT', 'LIVE']

        # Convert product types to readable format
        product_categories = [dict(Product.PRODUCT_TYPES)[ptype] for ptype in product_categories]

        # Combine and remove duplicates
        categories = list(set(animal_categories + product_categories))
        
        return JsonResponse({"categories": categories}, safe=False)
