from django.contrib import admin
from .models import *

# Register your models here.
class receipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image_url', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SalesAdmin(admin.ModelAdmin):
    list_display = ['id', 'profit', 'expenditure']

admin.site.register(Receipe, receipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sales,SalesAdmin)
admin.site.register(Product)
admin.site.register(Order)
