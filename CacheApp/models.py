from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Receipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='receipe')
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255)
    description = models.TextField()
    added_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
class Sales(models.Model):
    receipe = models.ForeignKey(Receipe, on_delete=models.CASCADE, related_name='sales')
    profit = models.PositiveIntegerField()
    expenditure = models.PositiveIntegerField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    number_in_stock = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_items = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f'{self.product.name} x {self.number_of_items}'