from rest_framework import serializers
from .models import *
from Auth_System.models import Profile
# from Auth_System.serializers import ProfileSerializers
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
    user_id = serializers.IntegerField(source='post_creator.user.id', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)  # New field
    # Include the image field from the Profile model
    profile_image = serializers.CharField(source='post_creator.image', read_only=True)  # Access image from Profile

    class Meta:
        model = CreatePost
        fields = ['id', 'post_creator', 'user_id', 'image', 'video', 'caption', 'created_at', 'updated_at', 
                  'comments', 'likes', 'likes_count', 'profile_image']
  
    
    # class Meta:
    #     model = CreatePost
    #     fields = '__all__'
 
    