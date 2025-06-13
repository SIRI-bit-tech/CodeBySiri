from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Category, Project, Testimonial, Promise, ContactMessage, SeoSettings
from .forms import ContactForm


def home(request):
    """Main view for the home page with all sections"""
    categories = Category.objects.all()
    featured_projects = Project.objects.filter(is_published=True)[:6]

    # Get testimonials or promises based on configuration
    display_promises = Promise.objects.filter(
        is_published=True,
        display_instead_of_testimonials=True
    ).exists()

    if display_promises:
        testimonials = []
        promises = Promise.objects.filter(is_published=True)
    else:
        testimonials = Testimonial.objects.filter(is_published=True)
        promises = []

    contact_form = ContactForm()

    # Get SEO settings
    try:
        seo_settings = SeoSettings.objects.first()
    except:
        seo_settings = None

    context = {
        'categories': categories,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'promises': promises,
        'contact_form': contact_form,
        'seo_settings': seo_settings,
    }

    return render(request, 'portfolio/home.html', context)


def projects_list(request):
    """HTMX view for loading all projects"""
    projects = Project.objects.filter(is_published=True)

    if request.htmx:
        return render(request, 'portfolio/partials/projects_list.html', {'projects': projects})

    return render(request, 'portfolio/projects.html', {'projects': projects})


def projects_by_category(request, category_slug):
    """HTMX view for loading projects filtered by category"""
    category = get_object_or_404(Category, slug=category_slug)
    projects = Project.objects.filter(category=category, is_published=True)

    if request.htmx:
        return render(request, 'portfolio/partials/projects_list.html', {'projects': projects})

    return render(request, 'portfolio/projects.html', {
        'projects': projects,
        'category': category
    })


def project_detail(request, slug):
    """HTMX view for loading project details in a modal"""
    project = get_object_or_404(Project, slug=slug, is_published=True)

    if request.htmx:
        return render(request, 'portfolio/partials/project_detail.html', {'project': project})

    # Fallback for direct URL access
    return render(request, 'portfolio/project_detail.html', {'project': project})


def testimonials_list(request):
    """HTMX view for loading more testimonials"""
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 3))

    # Get testimonials or promises based on configuration
    display_promises = Promise.objects.filter(
        is_published=True,
        display_instead_of_testimonials=True
    ).exists()

    if display_promises:
        testimonials = []
        promises = Promise.objects.filter(is_published=True)[offset:offset + limit]
        has_more = Promise.objects.filter(is_published=True).count() > offset + limit
    else:
        testimonials = Testimonial.objects.filter(is_published=True)[offset:offset + limit]
        promises = []
        has_more = Testimonial.objects.filter(is_published=True).count() > offset + limit

    context = {
        'testimonials': testimonials,
        'promises': promises,
        'has_more': has_more,
        'next_offset': offset + limit,
        'limit': limit,
    }

    return render(request, 'portfolio/partials/testimonials_list.html', context)


def contact_submit(request):
    """HTMX view for handling contact form submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send email notification to website owner
            try:
                # Email to website owner
                owner_subject = f"New Contact Message: {contact_message.subject}"
                owner_message = render_to_string('portfolio/emails/contact_notification.txt', {
                    'contact': contact_message,
                })
                send_mail(
                    owner_subject,
                    owner_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  # Send to website owner
                    fail_silently=False,
                )

                # Confirmation email to the sender
                user_subject = f"Thank you for contacting CodeBySiri"
                user_message = render_to_string('portfolio/emails/contact_confirmation.txt', {
                    'name': contact_message.name,
                })
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],  # Send to the person who submitted the form
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't show to user
                print(f"Email sending failed: {e}")

            # Return success message with a fresh form for HTMX
            return render(request, 'portfolio/partials/contact_success.html', {'form': ContactForm()})
        else:
            # Return form with errors for HTMX
            return render(request, 'portfolio/partials/contact_form.html', {'form': form})

    # If not POST, return empty form
    return render(request, 'portfolio/partials/contact_form.html', {'form': ContactForm()})
