from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"

class Product(models.Model):
    mainimage = models.ImageField(upload_to='Product')
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_text = models.TextField(max_length=200, verbose_name='Preview text')
    details_text = models.TextField(max_length=200, verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def is_category(self):
        return Product.objects.filter(category =1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created',]