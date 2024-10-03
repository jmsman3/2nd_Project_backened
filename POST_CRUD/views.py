from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from POST_CRUD.models import CreatePost,LikePost,CommentPost,Profile
from POST_CRUD.serializers import PostSerializer,LikeSerializer,CommentSeralizer 
from Auth_System.serializers import ProfileSerializers,PostSerializer , FollowSerializer
from Auth_System.models import Follow
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404 
from rest_framework.permissions import IsAuthenticated
# Create your views here.
#----------> Get , Post , Put ,Patch, Delete for Post View



class Specific_USer_Posts_Find_View(APIView):
    def get(self,request, format=None, user_id=None):    
        if user_id: #get all post for a specific user
            try:
                user = User.objects.get(id=user_id)
                print("User:" , user)

                profile = get_object_or_404(Profile, user=user)
                print("profile:" , profile)

                post = CreatePost.objects.filter(post_creator=profile)
                serializer = PostSerializer(post,many=True)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except CreatePost.DoesNotExist:
                return Response({'error' : 'Post Does not Exist'} , status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response({'error' : 'User id not found'} , status=status.HTTP_400_BAD_REQUEST)
        
class PostApiView(APIView):
    permission_classes =[IsAuthenticatedOrReadOnly]
    #Specific post get
    def get(self, request, format=None , pk=None , user_id=None):
        if pk:
            try:
                post = CreatePost.objects.get(pk = pk) #Specific post get kora
                serializer = PostSerializer(post)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except CreatePost.DoesNotExist:
                return Response({'error' : 'Post Does not Exist'} , status=status.HTTP_400_BAD_REQUEST)
            
        else:  #All Post get kora
            try:
                posts = CreatePost.objects.all()  
                serializer = PostSerializer(posts ,many=True)
                return Response(serializer.data , status=status.HTTP_200_OK)
            except CreatePost.DoesNotExist:
                return Response({'error':'Post Does not Exist'} , status=status.HTTP_400_BAD_REQUEST)
    # Post korar jabe
    def post(self,request,format=None,pk=None):
        data = request.data 
        print(request.user)
        try:
            data['post_creator'] = request.user.profile
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(post_creator=request.user.profile)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    #Post update kora jabe
    def put(self,request,format=None,pk=None):
        try:
            if pk:
                post = CreatePost.objects.get(pk=pk)
                if post.post_creator !=  request.user.profile:
                    return Response({'error' : 'Permission denied'},status=status.HTTP_403_FORBIDDEN)
                serializer = PostSerializer(post,data=request.data , partial=False)
                if serializer.is_valid():
                    serializer.save()
                    return Response (serializer.data ,status=status.HTTP_200_OK)
                return Response (serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
            return Response({'error' :"User Does not Exist"} , status=status.HTTP_400_BAD_REQUEST)
        except CreatePost.DoesNotExist:
            return Response({'error':'Post Does Not exist'} , status = status.HTTP_404_NOT_FOUND)
                
    #olpo kechu update kora jabe
    def patch(self,request,format=None,pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            if post.post_creator != request.user.profile:
                return Response({'error' : 'You are not the Owner of this Post,Permission Denied'} , status=status.HTTP_400_BAD_REQUEST)
        
            serializer = PostSerializer(post , data= request.data ,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_200_OK)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except CreatePost.DoesNotExist:
            return Response({'error' : "Post Does Not Exist"} , status=status.HTTP_404_NOT_FOUND)
       
    def delete(self,request , format=None, pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            if post.post_creator != request.user.profile:
                return Response({'error' : 'Permission Denied'} , status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({'message' : "Post deleted Successfully"} , status=status.HTTP_204_NO_CONTENT)
        except CreatePost.DoesNotExist:
            return Response({'error':'Post Does not Exist'} , status=status.HTTP_404_NOT_FOUND)


#---------->POST ,DELETE for LikeVIEW 
# class LikeView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def post(self, request, format=None, pk=None):
#         try:
#             post = CreatePost.objects.get(pk=pk)
#             if LikePost.objects.filter(likepost=post, liked_by=request.user.profile).exists():
#                 return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 LikePost.objects.create(likepost=post, liked_by=request.user.profile)
#                 return Response({
#                     'message': 'Liked post successfully',
#                     'likes_count': post.likes_count  # Return updated likes count
#                 }, status=status.HTTP_201_CREATED)
#         except CreatePost.DoesNotExist:
#             return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, format=None, pk=None):
#         try:
#             post = CreatePost.objects.get(pk=pk)
#             like = LikePost.objects.get(likepost=post, liked_by=request.user.profile)
#             like.delete()
#             return Response({
#                 'message': 'Like removed successfully',
#                 'likes_count': post.likes_count  # Return updated likes count
#             }, status=status.HTTP_204_NO_CONTENT)
#         except CreatePost.DoesNotExist:
#             return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         except LikePost.DoesNotExist:
#             return Response({'error': 'You haven’t liked this post'}, status=status.HTTP_404_NOT_FOUND)



class LikeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, format=None, pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            # Check if the user has already liked the post
            if LikePost.objects.filter(likepost=post, liked_by=request.user.profile).exists():
                return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the like
            LikePost.objects.create(likepost=post, liked_by=request.user.profile)

            print(f"Post {pk} liked by {request.user.username}")  # Debug logging
            # Return updated likes count
            return Response({
                'message': 'Liked post successfully',
                'likes_count': post.likes_count  # Return updated likes count
            }, status=status.HTTP_201_CREATED)

        except CreatePost.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error liking post: {e}")  # General error logging
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None, pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            # Attempt to retrieve the like
            like = LikePost.objects.get(likepost=post, liked_by=request.user.profile)
            like.delete()

            print(f"Post {pk} unliked by {request.user.username}")  # Debug logging
            # Return updated likes count
            return Response({
                'message': 'Like removed successfully',
                'likes_count': post.likes_count  # Return updated likes count
            }, status=status.HTTP_204_NO_CONTENT)

        except CreatePost.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except LikePost.DoesNotExist:
            return Response({'error': 'You haven’t liked this post'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error unliking post: {e}")  # General error logging
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#---------->COmment ApiView  - >GET, POST,PUT,DELETE      
class CommentApiVIew(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can post comments

    def post(self, request, pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            data = request.data
            data['commentpost'] = post.id
            
            # Check if user is authenticated and has a profile
            if request.user.is_authenticated:
                data['comment_by'] = request.user.profile.id 
            else:
                return Response({'error': 'You must be logged in to comment.'}, status=status.HTTP_403_FORBIDDEN)

            serializer = CommentSeralizer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CreatePost.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            comments = post.comments.all()  # Fetch all comments related to the post
            serializer = CommentSeralizer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CreatePost.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            comment = CommentPost.objects.get(pk=pk)
            if comment.comment_by != request.user.profile:
                return Response({'error': 'You are not the owner of this comment'}, status=status.HTTP_403_FORBIDDEN)

            comment.delete()
            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except CommentPost.DoesNotExist:
            return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        try:
            comment = CommentPost.objects.get(pk=pk)
            if comment.comment_by != request.user.profile:
                return Response({'error': 'You are not the owner of this comment'}, status=status.HTTP_403_FORBIDDEN)

            serializer = CommentSeralizer(comment, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CommentPost.DoesNotExist:
            return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)









# class CommentApiVIew(APIView):
#     permission_classes = [IsAuthenticated]  # Only authenticated users can post comments
#     def post(self, request, pk=None):
#         try:
#             post = CreatePost.objects.get(pk=pk)
#             data = request.data
#             data['commentpost'] = post.id

            
            
#             # Check if user is authenticated and has a profile
#             if request.user.is_authenticated:
#                 data['comment_by'] = request.user.profile.id 
#             else:
#                 return Response({'error': 'You must be logged in to comment.'}, status=status.HTTP_403_FORBIDDEN)

#             serializer = CommentSeralizer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except CreatePost.DoesNotExist:
#             return Response({'error': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        
#     def get(self, request, pk=None):
#         if pk:  # Get specific comment
#             try:
#                 comment = CommentPost.objects.get(pk=pk)
#                 serializer = CommentSeralizer(comment)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except CommentPost.DoesNotExist:
#                 return Response({'error': 'Sorry, Comment Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         else:  # Get all comments
#             comments = CommentPost.objects.all()
#             serializer = CommentSeralizer(comments, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
        
#     def put(self,request,pk=None):
#         try:
#             comment = CommentPost.objects.get(pk=pk)
#             if comment.comment_by != request.user.profile:
#                 return Response({'error':'permission denied'},status=status.HTTP_403_FORBIDDEN)
           
            
#             serializer = CommentSeralizer(comment, data=request.data, partial=False)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data , status=status.HTTP_200_OK)
#             return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
#         except CommentPost.DoesNotExist:
#             return Response({'error':'Comment Does not Exist'},status=status.HTTP_404_NOT_FOUND) 
        
        
#     def delete(self,request,pk=None):
#         try:
#             comment = CommentPost.objects.get(pk=pk)
#             if comment.comment_by != request.user.profile:
#                 return Response({'error':'permission denied'},status=status.HTTP_403_FORBIDDEN)
            
#             comment.delete()
#             return Response({'message':'Comment Deleted Successfully'} , status=status.HTTP_204_NO_CONTENT)
#         except CommentPost.DoesNotExist:
#             return Response({'error':'Comment Does not Exist'},status=status.HTTP_404_NOT_FOUND) 
   
    
# class CommentApiVIew(APIView):
    
#     def post(self, request, pk=None):
#         try:
#             post = CreatePost.objects.get(pk=pk)
#             data = request.data
#             data['commentpost'] = post.id
#             data['comment_by'] = request.user.profile.id 
#             serializer = CommentSeralizer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CreatePost.DoesNotExist:
#             return Response({'error': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        
    
#     def get(self, request, pk=None):
#         if pk:  
#             try:
#                 comment = CommentPost.objects.get(pk=pk)
#                 serializer = CommentSeralizer(comment)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except CommentPost.DoesNotExist:
#                 return Response({'error': 'Sorry, Comment Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         else:  
#             comments = CommentPost.objects.all()
#             serializer = CommentSeralizer(comments, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#     def put(self, request, pk=None):
#         try:
#             comment = CommentPost.objects.get(pk=pk)
#             if comment.comment_by != request.user.profile:
#                 return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#             serializer = CommentSeralizer(comment, data=request.data, partial=False)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except CommentPost.DoesNotExist:
#             return Response({'error': 'Comment Does not Exist'}, status=status.HTTP_404_NOT_FOUND)

    
#     def delete(self, request, pk=None):
#         try:
#             comment = CommentPost.objects.get(pk=pk)
#             if comment.comment_by != request.user.profile:
#                 return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
#             comment.delete()
#             return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except CommentPost.DoesNotExist:
#             return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
# class Particular_User_Apiview(APIView):
#     def get(self,request,user_id = None):
#         if user_id:
#             try:
#                 #get user profile 
#                 user = User.objects.get(id = user_id)
#                 profile = get_object_or_404(Profile, user=user)
#                 Profile_Serializer = ProfileSerializers(profile) #profile ta serialize korlam

#                 #get all post by the particular user
#                 posts = CreatePost.objects.filter(post_creator = profile)
#                 post_serializer = PostSerializer(posts , many=True)

#                 #get all likes by the particular user
#                 likes = LikePost.objects.filter(liked_by=profile)
#                 like_serializer = LikeSerializer(likes , many = True)

#                 #get all comment by the Particualr user
#                 comments = CommentPost.objects.filter(comment_by=profile)
#                 comment_serializer = CommentSeralizer(comments , many=True) 

#                 #get all followers and follwing by the particular user
#                 followers = Follow.objects.filter(following=profile)
#                 following = Follow.objects.filter(follower=profile)

#                 follower_serializer = FollowSerializer(followers,many=True)
#                 following_serializer = FollowSerializer(following, many=True)

#                 #all combine data 
#                 data={
#                     'profile' : Profile_Serializer.data,
#                     'posts' : post_serializer.data,
#                     'likes' : like_serializer.data,
#                     'comments' : comment_serializer.data,
#                     'followers' : follower_serializer.data,
#                     'following' : following_serializer.data,
#                 }
#                 return Response(data , status=status.HTTP_200_OK)
#             except Profile.DoesNotExist:
#                return Response({'error' : 'Profile Does Not Exist'} , status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'erros' : 'User id is not Provided here'} ,status=status.HTTP_400_BAD_REQUEST )

class Particular_User_Apiview(APIView):
    def get(self, request, user_id=None):
        if user_id:
            try:
                # Fetching the user instance, not the profile directly
                user = User.objects.get(id=user_id)
                profile = Profile.objects.get(user=user)  # Get the profile related to this user

                # Fetch all posts, likes, comments associated with the user through their profile
                posts = CreatePost.objects.filter(post_creator=profile)
                likes = LikePost.objects.filter(liked_by=profile)
                comments = CommentPost.objects.filter(comment_by=profile)

                # Now you making return the response containing all details
                return Response({
                    'profile': {
                        'id' : user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name,
                        
                    },
                    'More Bio-Data':{
                        'bio' : profile.bio,
                        'location': profile.location,
                        'mobile' : profile.mobile_no,

                    },
                    'posts': PostSerializer(posts, many=True).data,
                    'likes': LikeSerializer(likes, many=True).data,
                    'comments': CommentSeralizer(comments, many=True).data
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User id not provided'}, status=status.HTTP_400_BAD_REQUEST)





        
             







        



            

