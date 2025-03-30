from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class AnimalType(models.Model):
    """Model representing types of animals (e.g., Sheep, Goat, Chicken)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    age = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Supplier(models.Model):
    """Model representing suppliers of animals and products"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Product(models.Model):
    """Model for all animal products"""
    PRODUCT_TYPES = (
        ('LIVE', 'Live Animal'),
        ('MEAT', 'Meat'),
        ('EGG', 'Egg'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    age = models.PositiveIntegerField()
    product_type = models.CharField(max_length=4, choices=PRODUCT_TYPES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    suppliers = models.ManyToManyField(Supplier, related_name='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Live animal specific fields
    age = models.PositiveIntegerField(help_text="Age in months", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], blank=True, null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in kg", blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True, null=True)

    # Meat specific fields
    cut_type = models.CharField(max_length=100, help_text="E.g., Leg, Breast, Whole", blank=True, null=True)
    packaging = models.CharField(max_length=100, help_text="E.g., Vacuum sealed, Fresh", blank=True, null=True)
    weight_per_unit = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight per unit in kg", blank=True,
                                          null=True)
    is_frozen = models.BooleanField(default=False)

    # Egg specific fields
    size = models.CharField(max_length=20, choices=[
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    ], blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    quantity_per_pack = models.PositiveIntegerField(default=1, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_product_type_display()}"

    class Meta:
        ordering = ["name"]


class ProductImage(models.Model):
    """Images for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Inventory(models.Model):
    """Inventory management for products"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    last_restock_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory for {self.product.name}"

    class Meta:
        verbose_name_plural = "Inventory"


class InventoryTransaction(models.Model):
    """Tracks all inventory movements"""
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
    )

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.IntegerField()  # Can be positive or negative
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {abs(self.quantity)} - {self.inventory.product.name}"
