from django.contrib import admin
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


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured', 'stack_used')
    search_fields = ('name', 'description')
    filter_horizontal = ('stack_used',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'description')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'range')
    list_filter = ('category',)
    list_editable = ('range',)
    search_fields = ('title',)


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'date_earned')
    list_filter = ('date_earned',)
    search_fields = ('name', 'organization', 'description')


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('tier_name', 'price', 'delivery_time', 'is_popular', 'order')
    list_editable = ('is_popular', 'order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'read_time', 'published_at', 'is_published')
    list_filter = ('tag', 'is_published')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'budget', 'is_read', 'created_at')
    list_filter = ('service', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('created_at',)
