from rest_framework import serializers
from .models import Team, Registration, Article, FAQItem

class TeamSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Team 
        fields = "__all__"

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Registration 
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Article 
        fields = "__all__"

class FAQItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FAQItem 
        fields = "__all__"
