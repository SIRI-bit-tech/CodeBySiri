from django.conf import settings
from .models import SeoSettings


def seo_settings(request):
    """
    Add SEO settings to the template context
    """
    try:
        seo_settings_obj = SeoSettings.objects.first()
        if seo_settings_obj:
            return {
                'site_name': seo_settings_obj.site_title,
                'site_description': seo_settings_obj.site_description,
                'site_author': 'Siri',
                'site_keywords': seo_settings_obj.site_keywords,
                'site_url': f"https://{settings.META_SITE_DOMAIN}",
                'twitter_username': seo_settings_obj.twitter_site,
                'facebook_app_id': seo_settings_obj.facebook_app_id or '',
            }
    except Exception as e:
        # Log the error but don't break the site
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading SEO settings: {e}")

    # Fallback to default values
    return {
        'site_name': 'CodeBySiri',
        'site_description': 'Professional web development services with a focus on speed and quality delivery.',
        'site_author': 'Siri',
        'site_keywords': 'web development, django, python, responsive design, web design',
        'site_url': f"https://{settings.META_SITE_DOMAIN}",
        'twitter_username': '@codebysiri',
        'facebook_app_id': settings.META_FB_APPID,
    }
