from .import views
from django.urls import path,include

urlpatterns = [
    
    path('posts/' , views.PostApiView.as_view() , name='post_list'), #all post,new post
    path('posts/<int:pk>/',views.PostApiView.as_view() , name='post_list'),
    path('user/<int:user_id>/posts/',views.Specific_USer_Posts_Find_View.as_view(),name='user_posts'),

    path('posts/<int:pk>/like/',views.LikeView.as_view(),name='post-like'),

    path('posts/<int:pk>/comment/',views.CommentApiVIew.as_view(),name='post-comment'), # কমেন্ট পোস্ট করা এবং সব কমেন্ট দেখার URL

    path('comments/<int:pk>/',views.CommentApiVIew.as_view(),name='post-comment') # নির্দিষ্ট কমেন্ট দেখার, এডিট করার, এবং ডিলিট করার URL

]
