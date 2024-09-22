from django.contrib import admin
from .models import CreatePost,LikePost,CommentPost
# Register your models here.
admin.site.register(CreatePost)
admin.site.register(LikePost)
admin.site.register(CommentPost)