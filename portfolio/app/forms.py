from django.forms import ModelForm
from .models import (
    Project,
    Service,
    Skill,
    Formation,
    PricingPlan,
    FAQ,
    BlogPost,
    ContactMessage,
)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'


class FormationForm(ModelForm):
    class Meta:
        model = Formation
        fields = '__all__'


class PricingPlanForm(ModelForm):
    class Meta:
        model = PricingPlan
        fields = '__all__'


class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'


class ContactMessageForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'company', 'service', 'budget', 'timeline', 'message']
