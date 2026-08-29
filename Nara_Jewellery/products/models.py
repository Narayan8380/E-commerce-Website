from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    product_name    = models.CharField(max_length=200)
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description     = models.TextField(blank=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    image           = models.ImageField(upload_to='products/', blank=True, null=True)
    stock_quantity  = models.PositiveIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-created_at']  # newest products first

    def is_new(self):
        """
        Returns True if product was added
        in the last 14 days.
        """
        return self.created_at >= timezone.now() - timedelta(days=14)

class VisitRequest(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    product        = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                       null=True)
    user           = models.ForeignKey('auth.User', on_delete=models.SET_NULL,
                                       null=True, blank=True)
    name           = models.CharField(max_length=100)
    phone          = models.CharField(max_length=20)
    address        = models.TextField()
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True)
    message        = models.TextField(blank=True)
    status         = models.CharField(max_length=20,
                                      choices=STATUS_CHOICES,
                                      default='pending')
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.product} ({self.status})"

    class Meta:
        ordering = ['-created_at']

