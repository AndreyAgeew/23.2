from django.contrib import admin

from catalog.models import Product, Category, Contact, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "price", "category"
    list_display_links = "pk", "name"
    list_filter = ('category',)
    search_fields = "name", "description"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"


@admin.register(Contact)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "country", "inn", "address"


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = "pk", "get_product_names", "version_number", "version_name", "is_active"

    def get_product_names(self, obj):
        return '; '.join([product.name for product in obj.products.all()])
