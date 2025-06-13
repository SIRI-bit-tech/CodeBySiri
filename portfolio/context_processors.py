from django.conf import settings

def seo_settings(request):
    """
    Add SEO settings to the template context
    """
    return {
        'site_name': 'CodeBySiri',
        'site_description': 'Professional web development services with a focus on speed and quality delivery.',
        'site_author': 'Siri',
        'site_keywords': 'web development, django, python, responsive design, web design',
        'site_url': f"https://{settings.META_SITE_DOMAIN}",
        'twitter_username': '@codebysiri',
        'facebook_app_id': settings.META_FB_APPID,
    }
