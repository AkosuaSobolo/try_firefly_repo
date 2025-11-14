from django.contrib import admin
from .models import *

admin.site.register([Team, Registration, Article, Tag, FAQItem, Sponsor, GalleryItem])
