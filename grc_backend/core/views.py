from rest_framework import viewsets
from .models import Team, Registration, Article, FAQItem
from .serializers import TeamSerializer, RegistrationSerializer, ArticleSerializer, FAQItemSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQItem.objects.all()
    serializer_class = FAQItemSerializer
