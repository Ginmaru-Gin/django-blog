from django.contrib.auth.models import User
from rest_framework import serializers
from blog_posts.models import Post, Comment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, queryset=Post.objects.all(), view_name="post-detail")
    comments = serializers.HyperlinkedRelatedField(many=True, queryset=Comment.objects.all(), view_name="comment-detail")
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "posts", "comments"]
