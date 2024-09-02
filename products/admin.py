from django.contrib import admin
from .models import *

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pr_name', 'pr_price', 'available', 'stock')
    prepopulated_fields = {'pr_slug': ('pr_name',)}

@admin.register(productmetafield)
class ProductMetaFieldAdmin(admin.ModelAdmin):
    list_display = ('product', 'pr_measuring', 'pr_quantity', 'is_restrict')

@admin.register(product_images)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'pr_images')

# Register other models
admin.site.register(addmeal)
admin.site.register(Review)
admin.site.register(Email_m)
admin.site.register(BlogPost)
# admin.site.register(User)
