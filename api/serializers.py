from rest_framework import serializers
from stock_management.models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = serializers.CharField(source="animal_type.name")  # Get the category name from AnimalType
    type = serializers.CharField(source="get_product_type_display")  # Get the product type
    status = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'images', 'name', 'description', 'price', 'status', 'category', 'type', 'age']

    def get_images(self, obj):
        return [img.image.url for img in obj.images.all()]  # Return image URLs

    def get_status(self, obj):
        return "available" if obj.is_active else "sold"

    def get_age(self, obj):
        return f"{obj.age} months old" if obj.age else "N/A"




class OrderSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=255)  
    quantity = serializers.IntegerField(min_value=1)  # Ensures positive values
    unit_price = serializers.IntegerField(min_value=0)  # Ensures non-negative values
    fullname = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    delivery_address = serializers.CharField()
    whatsapp_number = serializers.BooleanField()  # Indicates if phone number is WhatsApp
    additional_info = serializers.CharField(required=False, allow_blank=True)
    
class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    company = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField()