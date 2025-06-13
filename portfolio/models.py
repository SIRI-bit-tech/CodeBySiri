from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from meta.models import ModelMeta


class SeoSettings(models.Model):
    """Model for storing global SEO settings"""
    site_title = models.CharField(max_length=100, default="CodeBySiri")
    site_description = models.TextField(
        default="Professional web development services with a focus on speed and quality delivery.")
    site_keywords = models.CharField(max_length=255,
                                     default="web development, django, python, responsive design, web design")
    og_image = CloudinaryField('image', folder='seo', null=True, blank=True)
    twitter_card = models.CharField(max_length=50, default="summary_large_image")
    twitter_site = models.CharField(max_length=50, default="@codebysiri")
    facebook_app_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "SEO Settings"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return "SEO Settings"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model, ModelMeta):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = CloudinaryField('image', folder='projects')
    live_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO fields
    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
        'url': 'get_absolute_url',
    }

    class Meta:
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description or self.description[:160]

    def get_meta_keywords(self):
        return self.meta_keywords or f"{self.category.name}, web development, portfolio"

    def get_meta_image(self):
        return self.image.url if self.image else None


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    testimonial_text = models.TextField()
    client_company = models.CharField(max_length=100, blank=True, null=True)
    client_photo = CloudinaryField('image', folder='testimonials', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"Testimonial from {self.client_name}"


class Promise(models.Model):
    text = models.TextField()
    is_published = models.BooleanField(default=True)
    display_instead_of_testimonials = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Promise: {self.text[:50]}..."


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"
