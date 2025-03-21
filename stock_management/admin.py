from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import (
    AnimalType,
    Supplier,
    Product,
    ProductImage,
    Inventory,
    InventoryTransaction
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'admin_thumbnail')
    readonly_fields = ('admin_thumbnail',)

    def admin_thumbnail(self, instance):
        if instance.image:
            return format_html('<img src="{}" width="100" height="auto" />', instance.image.url)
        return "No Image"


class InventoryInline(admin.StackedInline):
    model = Inventory
    can_delete = False
    fields = (('quantity', 'min_stock_level'), 'last_restock_date')


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'total_products', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    def total_products(self, obj):
        count = Product.objects.filter(animal_type=obj).count()
        url = (
                reverse('admin:core_product_changelist')
                + '?'
                + urlencode({'animal_type__id__exact': obj.id})
        )
        return format_html('<a href="{}">{} products</a>', url, count)

    total_products.short_description = 'Products'


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'is_active', 'total_supplied_products')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'contact_person', 'email', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')

    def total_supplied_products(self, obj):
        count = obj.products.count()
        url = (
                reverse('admin:core_product_changelist')
                + '?'
                + urlencode({'suppliers__id__exact': obj.id})
        )
        return format_html('<a href="{}">{} products</a>', url, count)

    total_supplied_products.short_description = 'Supplied Products'


class InventoryStatusFilter(admin.SimpleListFilter):
    title = 'inventory status'
    parameter_name = 'inventory_status'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Low Stock'),
            ('out', 'Out of Stock'),
            ('stocked', 'Well Stocked'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(
                inventory__quantity__gt=0,
                inventory__quantity__lte=models.F('inventory__min_stock_level')
            )
        if self.value() == 'out':
            return queryset.filter(inventory__quantity=0)
        if self.value() == 'stocked':
            return queryset.filter(
                inventory__quantity__gt=models.F('inventory__min_stock_level')
            )
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'get_animal_type', 'price', 'stock_status', 'is_active')
    list_filter = ('product_type', 'animal_type', 'is_active', InventoryStatusFilter)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('suppliers',)
    inlines = [ProductImageInline, InventoryInline]

    fieldsets = [
        (None, {
            'fields': ('name', 'slug', 'description', 'animal_type', 'product_type', 'price', 'suppliers', 'is_active')
        }),
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        # Add type-specific fieldsets based on product type
        if obj:
            if obj.product_type == 'LIVE':
                fieldsets.append(
                    ('Live Animal Details', {
                        'fields': (('age', 'gender'), ('weight', 'breed'))
                    })
                )
            elif obj.product_type == 'MEAT':
                fieldsets.append(
                    ('Meat Details', {
                        'fields': (('cut_type', 'packaging'), ('weight_per_unit', 'is_frozen'))
                    })
                )
            elif obj.product_type == 'EGG':
                fieldsets.append(
                    ('Egg Details', {
                        'fields': (('size', 'color'), 'quantity_per_pack')
                    })
                )

        fieldsets.append(
            ('Metadata', {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',)
            })
        )

        return fieldsets

    def get_animal_type(self, obj):
        return obj.animal_type.name

    get_animal_type.short_description = 'Animal Type'
    get_animal_type.admin_order_field = 'animal_type__name'

    def stock_status(self, obj):
        try:
            inventory = obj.inventory
            if inventory.quantity <= 0:
                return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
            elif inventory.quantity <= inventory.min_stock_level:
                return format_html('<span style="color: orange; font-weight: bold;">{} (Low)</span>',
                                   inventory.quantity)
            else:
                return format_html('<span style="color: green;">{}</span>', inventory.quantity)
        except Inventory.DoesNotExist:
            return format_html('<span style="color: gray;">No Inventory</span>')

    stock_status.short_description = 'Stock'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Create inventory record if it doesn't exist
        if not change:  # Only for new products
            if not hasattr(obj, 'inventory'):
                Inventory.objects.create(product=obj)


class InventoryTransactionInline(admin.TabularInline):
    model = InventoryTransaction
    extra = 1
    fields = ('transaction_type', 'quantity', 'supplier', 'notes', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'get_product_name', 'get_product_type', 'quantity', 'min_stock_level', 'stock_status', 'last_restock_date')
    list_filter = ('product__product_type', 'product__animal_type', 'last_restock_date')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [InventoryTransactionInline]

    def get_product_name(self, obj):
        return obj.product.name

    get_product_name.short_description = 'Product'
    get_product_name.admin_order_field = 'product__name'

    def get_product_type(self, obj):
        return obj.product.get_product_type_display()

    get_product_type.short_description = 'Type'
    get_product_type.admin_order_field = 'product__product_type'

    def stock_status(self, obj):
        if obj.quantity <= 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif obj.quantity <= obj.min_stock_level:
            return format_html('<span style="color: orange; font-weight: bold;">Low Stock</span>')
        else:
            return format_html('<span style="color: green;">Well Stocked</span>')

    stock_status.short_description = 'Status'


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product', 'transaction_type', 'quantity', 'get_supplier', 'created_at')
    list_filter = ('transaction_type', 'created_at', 'inventory__product__product_type')
    search_fields = ('inventory__product__name', 'notes', 'supplier__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def get_product(self, obj):
        return obj.inventory.product.name

    get_product.short_description = 'Product'
    get_product.admin_order_field = 'inventory__product__name'

    def get_supplier(self, obj):
        if obj.supplier:
            return obj.supplier.name
        return "-"

    get_supplier.short_description = 'Supplier'
    get_supplier.admin_order_field = 'supplier__name'


# Customize the admin site
admin.site.site_header = "Gyamfi Farms & Agro Ventures Admin"
admin.site.site_title = "Gyamfi Farms Admin Portal"
admin.site.index_title = "Welcome to Gyamfi Farms Management System"
