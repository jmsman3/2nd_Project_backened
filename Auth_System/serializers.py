from rest_framework import serializers
from .models import Profile ,Follow
from django.contrib.auth.models import User
from POST_CRUD.serializers import PostSerializer
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username']

class ProfileSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    first_name = serializers.CharField(source = 'user.first_name' ,read_only = True)
    last_name = serializers.CharField(source = 'user.last_name' , read_only=True)
    email = serializers.CharField(source = 'user.email' , read_only = True)
   
    class Meta:
        model = Profile
        # fields = ['id' ,'user' ,'first_name' , 'last_name' ,'bio','location','mobile_no','image']
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']

        if password != password2:
            raise serializers.ValidationError({'error' :"Password Doesn't match"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already Exist"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Usernaem Already Exist'})
        account = User(username=username,email=email,first_name=first_name ,last_name=last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required= True)

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

#Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source = 'follower.username')
    following = serializers.ReadOnlyField(source = 'following.username')

    class Meta:
        model = Follow
        fields = ['follower' , 'following']
