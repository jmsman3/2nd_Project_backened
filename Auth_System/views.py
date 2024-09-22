from django.shortcuts import render ,redirect
from rest_framework import viewsets
from .models import Profile, Follow
from .serializers import ProfileSerializers ,RegistrationSerializer,UserLoginSerializer ,FollowSerializer
from rest_framework.views import APIView
#add
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
#email
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives,send_mail
#authenticate
from .models import Profile
from django.contrib.auth import authenticate ,login,logout
from rest_framework.authtoken.models import Token
# Create your views here.
from rest_framework import filters,pagination 
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
#Filter
class SpecificPerson(filters.BaseFilterBackend):
    def filter_queryset(self,request , queryset , view):
        user_id   = request.query_params.get("user_id")
        if user_id  :
            print(f"Filtering by user_id: {user_id}")  #debug
            return queryset.filter(user__id=user_id)
        return queryset
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    
    filter_backends=[SpecificPerson]

    
    def perform_create(self, serializer):
        user_id = self.request.data.get('user')   #user id ta ber kore anlam 
        user = User.objects.get(id=user_id)  
        serializer.save(user=user)

class ProfileDetails(APIView):
    def get(self,request,id):
        user = User.objects.get(pk=id)
        Profileuser = Profile.objects.get(user=user) 
        serializer = ProfileSerializers(Profileuser)
        return Response(serializer.data)
    
    def put(self,request,id):
        user = User.objects.get(pk=id)



class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self,request):
        serializer = self.serializer_class(data = request.data)
      
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            confirm_link = f"http://127.0.0.1:8000/user/active/{uid}/{token}"
            print(confirm_link)
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_eamil.html', {'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check Your Email for Confirmation")
        return Response(serializer.errors)
    
def activate(request ,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('http://127.0.0.1:5500/login.html')
    else:
        return redirect('http://127.0.0.1:5500/signup.html') 


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Check if the username exists in the database
            user_exists = User.objects.filter(username=username).exists()

            if user_exists:
                user = authenticate(username=username, password=password)
                if user:
                    # If user exists and password is correct
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request, user)
                    return Response({'token': token.key, 'user_id': user.id})
                else:
                    # Username is correct, but password is incorrect
                    return Response({'error': 'incorrect_password'})
            else:
                # Check if the password is also incorrect
                user_with_password = User.objects.filter(password=password).exists()
                
                if not user_with_password:
                    # Both username and password are wrong
                    return Response({'error': 'Both Username namd Password is Wrong,invalid_credentials'})
                else:
                    # Only the username is incorrect
                    return Response({'error': 'incorrect_username'})
        else:
            return Response(serializer.errors)

class USerLogoutApiview(APIView):
    def get(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')


class FollowAPIview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        user_to_follow = get_object_or_404(User, id =id)
        follow, created = Follow.objects.get_or_create(follower = request.user , following = user_to_follow)

        if created:
            serializer = FollowSerializer(follow)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response({"message" : "Already Following this User"} , status=status.HTTP_400_BAD_REQUEST)

class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request ,id):
        user_to_unfollow = get_object_or_404(User ,id =id)
        #check bortoman user onno user k follow kore kina
        follow = Follow.objects.filter(follower = request.user , following = user_to_unfollow)

        if follow.exists():
            #jodi follow kore taile delete
            follow.delete()
            return Response({"message" : "Unfollow Successfully"} , status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message" : "You are not following this User"} , status=status.HTTP_400_BAD_REQUEST)
