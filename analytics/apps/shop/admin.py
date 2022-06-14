from django.contrib import admin

from apps.shop.models import Category, Brand, Product, ProductImages


admin.site.register([Brand, Category, ProductImages])


class ProductImageInline(admin.TabularInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
