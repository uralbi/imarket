from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    def get_absolute_url(self):
        return reverse('by_category', kwargs={"category_id": self.pk})

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('category_name',)


    def __str__(self):
        return self.category_name