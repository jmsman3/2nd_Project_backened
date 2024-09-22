from .import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.UserRegistrationApiView.as_view(),name="register"),
    path('login/',views.UserLoginApiView.as_view(),name="login"),
    path('logout/',views.USerLogoutApiview.as_view(),name="logout"),
    path('active/<uid64>/<token>/' ,views.activate, name='active'),
    path('user_details/<int:id>/' ,views.ProfileDetails.as_view(), name='user_Details'),
    # path('all/' ,views.ProfileViewSet.as_view(), name='profile_all'),


    path('follow/<int:id>/' ,views.FollowAPIview.as_view(), name='follow'),
    path('unfollow/<int:id>/' ,views.UnfollowAPIView.as_view(), name='unfollow'),
]
