from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify


class Stack(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tech Stack'
        verbose_name_plural = 'Tech Stacks'

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ai', 'AI & ML'),
        ('fullstack', 'Full-Stack Web'),
        ('backend', 'APIs & FinTech'),
        ('cloud', 'Cloud & DevOps'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='fullstack',
    )
    description = models.TextField()
    image_1 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='projects/', blank=True, null=True)
    stack_used = models.ManyToManyField(Stack, blank=True, related_name='projects')
    live_url = models.URLField(blank=True, null=True, help_text="Live project or demo URL")
    github_url = models.URLField(blank=True, null=True, help_text="GitHub repository URL")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(
        max_length=60,
        default='fa-solid fa-code-branch',
        help_text="Font Awesome icon class (e.g. 'fa-solid fa-robot')",
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title}"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend & Architecture'),
        ('ai', 'AI, Machine Learning & Data'),
        ('frontend', 'Frontend & Design Systems'),
        ('devops', 'Databases, Cloud & DevOps'),
    ]

    title = models.CharField(max_length=100)
    range = models.IntegerField(
        default=85,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency percentage between 0 and 100",
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='backend',
    )

    class Meta:
        ordering = ['-range', 'title']

    def __str__(self):
        return f"{self.title} ({self.range}%)"


class Formation(models.Model):
    name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, blank=True, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='formations/', blank=True, null=True)
    date_earned = models.DateField()

    class Meta:
        ordering = ['-date_earned']
        verbose_name = 'Formation / Certification'
        verbose_name_plural = 'Formations & Certifications'

    def __str__(self):
        return f"{self.name} - {self.date_earned}"


class PricingPlan(models.Model):
    tier_name = models.CharField(max_length=100)
    price = models.CharField(max_length=50, help_text="e.g. $150+, $700+, $1,000+")
    period = models.CharField(max_length=50, default='/ starting at')
    description = models.TextField()
    features = models.TextField(help_text="Enter one feature per line")
    delivery_time = models.CharField(max_length=100, blank=True, default='1–2 Weeks Delivery')
    is_popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    def __str__(self):
        return f"{self.tier_name} ({self.price})"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tag = models.CharField(max_length=80, default='AI Engineering')
    summary = models.TextField()
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    published_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', '-id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=150, blank=True, default='')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    budget = models.CharField(max_length=100, blank=True, default='')
    timeline = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at:%Y-%m-%d}"
