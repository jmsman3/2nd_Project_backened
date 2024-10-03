from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
#Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile' )
    bio = models.TextField(max_length=200 ,default="")
    location = models.CharField(max_length=100,blank=True ,default="")
    mobile_no = models.CharField(max_length=12 ,default="")
    image = models.URLField(max_length=300 )
    # default="https://i.ibb.co.com/Jkcfb1W/png-transparent-user-profile-computer-icons-login-user-avatars-thumbnail.png"
    # created_at = models.DateTimeField( default=timezone.now,auto_now_add=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    class Meta:
        verbose_name_plural = "Profile User"

#Follow Model
class Follow(models.Model):
    follower = models.ForeignKey(User , on_delete=models.CASCADE , related_name='following')
    following = models.ForeignKey(User , on_delete=models.CASCADE ,related_name='followers')

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['follower','following'] , name='unique_follower_following')]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
 
