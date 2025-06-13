from django.contrib import admin
from .models import Category, Project, Testimonial, Promise, ContactMessage, SeoSettings


@admin.register(SeoSettings)
class SeoSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic SEO', {
            'fields': ('site_title', 'site_description', 'site_keywords')
        }),
        ('Social Media', {
            'fields': ('og_image', 'twitter_card', 'twitter_site', 'facebook_app_id')
        }),
    )

    def has_add_permission(self, request):
        # Check if any SeoSettings object exists
        count = SeoSettings.objects.count()
        return count == 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'display_order', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('display_order', 'is_published')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image', 'live_url', 'category', 'display_order', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'display_order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('client_name', 'testimonial_text', 'client_company')
    list_editable = ('display_order', 'is_published')


@admin.register(Promise)
class PromiseAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'is_published', 'display_instead_of_testimonials')
    list_filter = ('is_published', 'display_instead_of_testimonials')
    list_editable = ('is_published', 'display_instead_of_testimonials')

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Text'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False
