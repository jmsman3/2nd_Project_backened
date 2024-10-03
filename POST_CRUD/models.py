from django.db import models
from django.contrib.auth.models import User
from Auth_System.models import Profile

# Create your models here.

#Post creating Model
class CreatePost(models.Model):
    post_creator = models.ForeignKey(Profile , on_delete=models.CASCADE , related_name='user_post')

    image = models.URLField(max_length=300 , blank=True , null=True )
    video = models.URLField(max_length=300 , blank=True , null=True )
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"post created by {self.post_creator.user.username}"
    
    @property
    def likes_count(self):
        return self.likes.count()
    
# Post Like Model 
class LikePost(models.Model):
    likepost = models.ForeignKey(CreatePost , on_delete=models.CASCADE , related_name='likes')
    liked_by = models.ForeignKey(Profile ,on_delete=models.CASCADE)

    def __str__(self):
        return f"Post liked by {self.liked_by.user.username}"
    
#Post Comment Model
class CommentPost(models.Model):
    commentpost = models.ForeignKey(CreatePost , on_delete=models.CASCADE , related_name='comments')
    comment_by  = models.ForeignKey(Profile , on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"Post Commented by {self.comment_by.user.username}"
    