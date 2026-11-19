import logging
from smtplib import SMTPException

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from .models import (
    Stack,
    Project,
    Service,
    Skill,
    Formation,
    PricingPlan,
    FAQ,
    BlogPost,
    ContactMessage,
)

logger = logging.getLogger(__name__)


def _save_contact_submission(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    message_text = request.POST.get('message', '').strip()
    company = request.POST.get('company', '').strip()
    service_id = request.POST.get('service', '').strip()
    service = Service.objects.filter(pk=service_id).first() if service_id.isdecimal() else None
    budget = request.POST.get('budget', '').strip()
    timeline = request.POST.get('timeline', '').strip()


    if name and email and message_text:
        ContactMessage.objects.create(
            name=name,
            email=email,
            company=company,
            service=service,
            budget=budget,
            timeline=timeline,
            message=message_text,
        )

        service_label = service.title if service else 'General inquiry'
        subject = f"New portfolio inquiry from {name}"
        full_message = (
            f"From: {name} <{email}>\n"
            f"Company: {company or 'Not provided'}\n"
            f"Service: {service_label}\n"
            f"Budget: {budget or 'Not provided'}\n"
            f"Timeline: {timeline or 'Not provided'}\n\n"
            f"Message:\n{message_text}"
        )

        try:
            EmailMessage(
                subject=subject,
                body=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['madilaelyamine@gmail.com'],
                reply_to=[email],
            ).send(fail_silently=False)
        except (OSError, SMTPException):
            logger.exception('Could not send contact inquiry notification email')
            return name, email, False

        return name, email, True
    return None, None, False


def home_view(request):
    if request.method == 'POST':
        name, _, email_sent = _save_contact_submission(request)
        if name:
            if email_sent:
                messages.success(
                    request,
                    f"Thank you, {name}! Your message has been saved. I'll get back to you within 24 hours."
                )
            else:
                messages.warning(
                    request,
                    "Your message was saved, but the email notification could not be sent. Please try again later."
                )
            return redirect('/#contact')

    context = {
        'projects': Project.objects.prefetch_related('stack_used').all(),
        'services': Service.objects.all(),
        'skills': Skill.objects.all(),
        'stacks': Stack.objects.all(),
        'pricing_plans': PricingPlan.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'pages/home.html', context)


def projects_view(request):
    projects = Project.objects.prefetch_related('stack_used').all()
    category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '').strip()

    if category in dict(Project.CATEGORY_CHOICES):
        projects = projects.filter(category=category)

    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(stack_used__name__icontains=search_query)
        ).distinct()

    paginator = Paginator(projects, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'projects': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'selected_category': category,
        'search_query': search_query,
    }
    return render(request, 'pages/projects.html', context)


def about_view(request):
    context = {
        'skills': Skill.objects.all(),
        'stacks': Stack.objects.all(),
        'formations': Formation.objects.all(),
        'blog_posts': BlogPost.objects.filter(is_published=True),
    }
    return render(request, 'pages/about.html', context)


def services_view(request):
    context = {
        'services': Service.objects.all(),
        'pricing_plans': PricingPlan.objects.all(),
    }
    return render(request, 'pages/services.html', context)


def contact_view(request):
    if request.method == 'POST':
        name, email, email_sent = _save_contact_submission(request)
        if name:
            if email_sent:
                messages.success(
                    request,
                    f"Thank you, {name}! Your inquiry has been saved. I'll respond to {email} within 24 hours."
                )
            else:
                messages.warning(
                    request,
                    "Your inquiry was saved, but the email notification could not be sent. Please try again later."
                )
            return redirect('contact')

    return render(request, 'pages/contact.html', {'services': Service.objects.all()})
