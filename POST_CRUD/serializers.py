from rest_framework import serializers
from .models import *

class CommentSeralizer(serializers.ModelSerializer):
    # commentpost = serializers.StringRelatedField()
    # comment_by = serializers.StringRelatedField()
    class Meta:
        model = CommentPost
        fields = '__all__'
class LikeSerializer(serializers.ModelSerializer):
    likepost = serializers.StringRelatedField(many=False)
    liked_by = serializers.StringRelatedField(many=False)
    class Meta:
        model = LikePost
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSeralizer(many = True , read_only = True)
    likes = LikeSerializer(many=True , read_only = True)
    post_creator = serializers.StringRelatedField()
    
    class Meta:
        model = CreatePost
        fields = '__all__'

    
    