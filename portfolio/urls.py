from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Main views
    path('', views.home, name='home'),

    # HTMX views for partial content loading
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<slug:category_slug>/', views.projects_by_category, name='projects_by_category'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('testimonials/', views.testimonials_list, name='testimonials_list'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
]
