from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.HyperlinkedRelatedField(many=True, queryset=Comment.objects.all(), view_name="comment-detail")
    class Meta:
        model = Post
        fields = "__all__"
        ordering = ["-date"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        ordering = ["-date"]
    