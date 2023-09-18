from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    class Meta:
        ordering = ["-created_at"]

    name = models.CharField(max_length=200)
    description = models.TextField()
    preview_description = models.TextField()
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

    def get_preview(self):
        return self.preview_description.split('-')[1:]

    def short_desription(self):
        return self.description[:100] + '...'


class Contact(models.Model):
    country = models.CharField(max_length=100)
    inn = models.CharField(max_length=12)
    address = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.country} ({self.address})"


class Version(models.Model):
    products = models.ManyToManyField(Product, related_name='versions', blank=True)
    number = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
