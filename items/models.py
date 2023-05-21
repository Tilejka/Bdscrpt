from django.db import models

from users.models import User


class ItemCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Quality(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'quality'
        verbose_name_plural = 'qualities'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(null=True, blank=True)
    quality = models.ForeignKey(to=Quality, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items_images')
    category = models.ForeignKey(to=ItemCategory, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    favourite = models.ManyToManyField(to=User, related_name='favourite', blank=True)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return self.name
