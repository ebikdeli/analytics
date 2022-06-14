from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from taggit.managers import TaggableManager
from django_quill.fields import QuillField
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField

import uuid


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('category'))
    sub = models.ForeignKey(to='self',
                            on_delete=models.CASCADE,
                            verbose_name=_('sub_category'),
                            null=True,
                            blank=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    background_image = models.ImageField(verbose_name=_('background image'), blank=True, null=True)
    tags = TaggableManager(verbose_name=_('tags'), blank=True)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    country = CountryField(verbose_name=_('country'), blank=True, null=True)
    logo = models.ImageField(verbose_name=_('logo'), blank=True, null=True)
    founder = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('founder'))
    tags = TaggableManager(verbose_name=_('tags'), blank=True)
    slug = models.SlugField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductManager(models.Manager):
    """Custom product manager to implement DRY in views"""
    def is_enough_in_stock(self, product_id, numbers):
        """Check if enough products are in stock for the type of specific product"""
        prod_query = self.get_queryset().filter(product_id=product_id)
        if prod_query:
            product = prod_query.first()
            if product.in_stock >= numbers:
                return product
        return None

    def return_to_stock(self, product_id, numbers):
        """return items from user's cart to the stock"""
        prod_query = self.get_queryset().filter(product_id=product_id)
        if prod_query:
            product = prod_query.first()
            product.in_stock += numbers
            product.save()


class Product(models.Model):
    product_id = models.CharField(default=uuid.uuid4, max_length=36, verbose_name=_('product id'))
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products_category',
                                 verbose_name=_('category'))
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name='products_brand',
                              verbose_name=_('brand'))
    name = models.CharField(max_length=50, verbose_name=_('product name'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=9, decimal_places=0)
    in_stock = models.PositiveIntegerField(verbose_name=_('stock'), default=0)
    is_available = models.BooleanField(verbose_name=_('available'), default=False)
    discount_percent = models.DecimalField(verbose_name=_('product discount(percent)'), default=0, max_digits=5,
                                           decimal_places=2,
                                           validators=[
                                               MaxValueValidator(100, _('percent could not be more than 100')),
                                               MinValueValidator(0, _('percent could not be less than 0'))
                                           ])
    discount_value = models.DecimalField(verbose_name=_('discount_value'), default=0, max_digits=9, decimal_places=0)
    is_special_offer = models.BooleanField(verbose_name=_('is special offer'), default=False)
    image = models.ImageField(verbose_name=_('image'), blank=True, null=True)
    end_price = models.DecimalField(verbose_name=_('end price'), default=0, max_digits=9, decimal_places=0)
    tags = TaggableManager(verbose_name=_('tags'), blank=True)
    overview = QuillField(verbose_name=_('overview'), blank=True, null=True)
    # review = QuillField(verbose_name=_('review'), blank=True, null=True)
    review = RichTextField(verbose_name=_('review'), blank=True, null=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    objects = ProductManager()

    class Meta:
        ordering = ['-updated', 'is_available']

    def __str__(self):
        return f'{self.brand.name}_{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand.name}_{self.name}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        pass


class ProductImages(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='product_images',
                                verbose_name=_('product'))
    image = models.ImageField(verbose_name=_('image'), null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.product.brand.name}_{self.product.name}_image{self.id}'
