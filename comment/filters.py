import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    class Meta:
        fields = {'content_type': ['exact'], }
        model = Post
