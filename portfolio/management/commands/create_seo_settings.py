from django.core.management.base import BaseCommand
from portfolio.models import SeoSettings


class Command(BaseCommand):
    help = 'Create default SEO settings if none exist'

    def handle(self, *args, **options):
        if not SeoSettings.objects.exists():
            SeoSettings.objects.create(
                site_title="CodeBySiri",
                site_description="Professional web development services with a focus on speed and quality delivery.",
                site_keywords="web development, django, python, responsive design, web design",
                twitter_card="summary_large_image",
                twitter_site="@codebysiri"
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created default SEO settings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('SEO settings already exist')
            )
