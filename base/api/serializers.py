from rest_framework.serializers import ModelSerializer
from base.models import Room, Article

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'created']