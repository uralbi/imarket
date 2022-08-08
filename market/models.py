from django.db import models
from category.models import Category
from accounts.models import Account
from django.urls import reverse
from .image_process import image_process

class Item(models.Model):
    STATUS = (
        ('Selling', 'selling'),
        ('Buying', 'buying'),
        ('Renting', 'renting'),
        ('For Rent', 'for rent'),
    )
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    image1 = models.ImageField(upload_to='media/item_pics/%Y/%m/%d', default = 'default_image.png')
    price = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Selling')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image1:
            image_process(self.image1.path)

    def delete(self, *args, **kwargs):
        if self.image1 and 'default_image' not in self.image1.name:
            self.image1.delete()
        if ItemGallery.objects.filter(item = self.id).exists():
            images = ItemGallery.objects.filter(item = self.id)
            for image in images:
                image.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('item_detail_view', kwargs={"pk": self.pk})


class ItemGallery(models.Model):
    item = models.ForeignKey(Item, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/item_pics/%Y/%m/%d', max_length=255)

    def __str__(self):
        return self.item.item_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image_process(self.image.path)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)


    class Meta:
        verbose_name = 'Item Gallery'
        verbose_name_plural = 'Item Gallery'


class SavedItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "item"]

    def __str__(self):
        name = f'{self.user}-{self.item.item_name[:10]}'
        return name