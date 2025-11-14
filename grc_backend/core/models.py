from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# --- Mixins ---

class TimeStamped(models.Model):
    """Abstract base class for models that need creation/modification timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated On")
    
    class Meta: 
        abstract = True
        ordering = ['-created_at'] # Default ordering by creation time

# --- Team Models ---

class Team(TimeStamped):
    # Defined here so it's easily accessible by other models like GalleryItem
    CATEGORY_CHOICES = [
        ("techs", "Techs League"),
        ("stars", "Stars League"),
        ("engineers", "Engineers League"),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="A URL-friendly identifier for the team.")
    school = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    
    # 1. Team Leader/Captain
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='captain_of_teams',
        verbose_name='Team Captain'
    )
    
    # 2. Team Roster (M2M for members)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='team_memberships',
        help_text="The other members of the team (excluding the captain)."
    )
    
    # FIX APPLIED: Changed 'help_name' to 'verbose_name'
    logo = models.ImageField(
        upload_to="team_logos/", 
        blank=True, 
        null=True, 
        verbose_name="Team Logo/Crest" 
    )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.school})"

class Registration(TimeStamped):
    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    # Changed to ForeignKey: A team might register multiple times for different events/years.
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending", db_index=True)
    documents = models.FileField(upload_to="registrations/", help_text="Upload official registration documents.")
    
    # Improvements for tracking and transparency
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_registrations', 
        verbose_name='Reviewed By'
    )
    rejection_reason = models.TextField(blank=True, help_text="Reason if the registration status is 'Rejected'.")
    
    class Meta:
        verbose_name = "Team Registration"
        verbose_name_plural = "Team Registrations"

    def __str__(self):
        return f"Registration for {self.team.name} - Status: {self.status}"

# --- Content Models ---

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True) # Added slug for tag URLs

    def __str__(self):
        return self.name

class Article(TimeStamped):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250, help_text="A short label used in URLs.")
    
    # 1. Publication Control
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)
    publish_date = models.DateTimeField(default=timezone.now, db_index=True)
    
    # 2. Featured Content
    featured_image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='published_articles'
    )
    content = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True, related_name='articles')
    
    # 3. SEO
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        help_text="SEO description (max 160 characters)."
    )
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        # Order by publish date, only show published status in primary view
        ordering = ['-publish_date'] 

    def __str__(self):
        return self.title

class FAQItem(TimeStamped):
    CATEGORY_CHOICES = [
        ("reg", "Registration"),
        ("rules", "Rules & Guidelines"),
        ("logistics", "Logistics & Schedule"),
        ("sponsor", "Sponsorship"),
        ("general", "General"),
    ]
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    
    # Improvements for sorting and visibility
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers appear first.")
    is_public = models.BooleanField(default=True, help_text="Check to display on the public FAQ page.")
    
    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        # Sort first by order, then by category
        ordering = ['order', 'category', 'question'] 

    def __str__(self):
        return self.question

# --- Partnership Models ---

class Sponsor(TimeStamped):
    TIER_CHOICES = [
        ("platinum", "Platinum"), # Added top tier
        ("gold", "Gold"),
        ("silver", "Silver"),
        ("bronze", "Bronze"),
    ]
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="Used for sponsor detail URLs (if needed).")
    logo = models.ImageField(upload_to="sponsors/")
    
    # 1. Website Link
    website_url = models.URLField(max_length=255, blank=True, help_text="The sponsor's official website link.")
    
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, db_index=True)
    description = models.TextField(blank=True)
    
    # 2. Control & Sorting
    is_active = models.BooleanField(default=True, help_text="Only show active sponsors on the website.")
    display_order = models.PositiveSmallIntegerField(default=0, help_text="Manual sort order within a tier.")

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        # Order by tier (to group gold first), then by manual order
        ordering = ['tier', 'display_order', 'name'] 

    def __str__(self):
        return f"{self.name} ({self.get_tier_display()})"


class GalleryItem(TimeStamped):
    MEDIA_CHOICES = [
        ("image", "Image (Upload to file)"),
        ("video_link", "Video (External URL)"), # Clarified purpose
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, db_index=True)
    
    # 1. Use separate fields for image file vs video URL
    image_file = models.ImageField(
        upload_to="gallery/images/", 
        blank=True, 
        null=True, 
        help_text="Upload file for Images."
    )
    video_url = models.URLField(
        max_length=255, 
        blank=True, 
        help_text="Paste YouTube/Video link for Videos."
    )
    
    # 2. Description and Context
    caption = models.CharField(max_length=250, blank=True, help_text="A short description for the media.")
    
    # References to which league and year the media belongs
    league = models.CharField(
        max_length=20, 
        choices=Team.CATEGORY_CHOICES, 
        db_index=True,
        verbose_name='League/Category'
    )
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(timezone.now().year + 2)],
        help_text="The year the media was taken."
    )
    
    class Meta:
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
        ordering = ['-year', 'league', '-created_at']

    def __str__(self):
        return f"{self.league} {self.year} - {self.caption or self.media_type}"