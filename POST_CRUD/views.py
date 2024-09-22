from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from POST_CRUD.models import CreatePost,LikePost,CommentPost,Profile
from POST_CRUD.serializers import PostSerializer,LikeSerializer,CommentSeralizer

# Create your views here.
#----------> Get , Post , Put ,Patch, Delete for Post View

class Specific_USer_Posts_Find_View(APIView):
    def get(self,request, format=None, user_id=None):    
        if user_id: #get all post for a specific user
            try:
                post = CreatePost.objects.filter(post_creator=user_id)
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
class LikeView(APIView):
    permission_classes =[IsAuthenticatedOrReadOnly]
    def post(self,request,format=None,pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            if LikePost.objects.filter(likepost=post , liked_by=request.user.profile).exists():
                return Response({'error' : 'You have already liked this post'},status=status.HTTP_400_BAD_REQUEST)
            else:
                LikePost.objects.create(likepost=post , liked_by=request.user.profile)
                return Response({'message':'Like post Successfully'} ,status=status.HTTP_201_CREATED)
        except:
            return Response({'error':'Post Does Not Exist'} , status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,foramt=None,pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            like =LikePost.objects.get(likepost = post,liked_by = request.user.profile)
            like.delete()
            return Response({'message' : 'Like Remove Successfull'} , status=status.HTTP_204_NO_CONTENT)
        except CreatePost.DoesNotExist:
            return Response({'error' : 'Post Does not Exist'},status=status.HTTP_404_NOT_FOUND)
        except LikePost.DoesNotExist:
            return Response({'error' : 'Sorry,You Havenot Liked this post'},status=status.HTTP_404_NOT_FOUND)

#---------->COmment ApiView  - >GET, POST,PUT,DELETE      

class CommentApiVIew(APIView):
    def post(self,request,pk=None):
        try:
            post = CreatePost.objects.get(pk=pk)
            data= request.data
            data['commentpost'] =post.id
            data['comment_by'] = request.user.profile.id 
            serializer = CommentSeralizer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except CreatePost.DoesNotExist:
            return Response({'error':'Post Does Not Exost'},status=status.HTTP_404_NOT_FOUND)
        
    def get(self,request,pk=None):
        if pk: #get specific comment
            try:
                comment = CommentPost.objects.get(pk=pk)
                serializer = CommentSeralizer(comment)
                return Response(serializer.data ,status=status.HTTP_200_OK)
            except CommentPost.DoesNotExist:
                return Response({'error':'Sorry,Comment Not Found'},status=status.HTTP_404_NOT_FOUND)
        else: #get all comments
            comments = CommentPost.objects.all()
            serializer = CommentSeralizer(comment , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        
        
    def put(self,request,pk=None):
        try:
            comment = CommentPost.objects.get(pk=pk)
            if comment.comment_by != request.user.profile:
                return Response({'error':'permission denied'},status=status.HTTP_403_FORBIDDEN)
           
            
            serializer = CommentSeralizer(comment, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_200_OK)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except CommentPost.DoesNotExist:
            return Response({'error':'Comment Does not Exist'},status=status.HTTP_404_NOT_FOUND) 
        
        
    def delete(self,request,pk=None):
        try:
            comment = CommentPost.objects.get(pk=pk)
            if comment.comment_by != request.user.profile:
                return Response({'error':'permission denied'},status=status.HTTP_403_FORBIDDEN)
            
            comment.delete()
            return Response({'message':'Comment Deleted Successfully'} , status=status.HTTP_204_NO_CONTENT)
        except CommentPost.DoesNotExist:
            return Response({'error':'Comment Does not Exist'},status=status.HTTP_404_NOT_FOUND) 
        
    
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

        
       

        



            

