from random import choices
from wsgiref import headers
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import *
from django.conf import settings
from django.core.mail import send_mail
from myapp.serializers import *
from .models import * 
from rest_framework import status
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import jwt, json
from .utils import *
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from django.db.models import Value, DateField
from django.contrib.auth.password_validation import validate_password
from rest_framework import pagination


# Create your views here.

class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self, data):
        response = Response(data)
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response




@api_view(['GET'])
def index(request):
    url_pattern ={

        'Index':'',
        'Register':'/register/',
        'Login':'/login/',
        'Logout':'/logout/',
        'Forgot Password':'/forgot-password/',
        'View Profile':'/view-profile/id',
        'Edit profile':'/edit-profile/',
        'Add Post':'/add-post/',
        'View Post':'/view-post/',
        'View One Post':'view-one-post/id',
        'Edit Post':'edit-post/id',
        'Delete Post':'delete-post/id',
        'Follow/Unfollow':'follow/id',
        'Like/Unlike':'like/id',
        'Comment':'comment/id',
        'View Comment':'view-comment/id',
        
    }
    return Response(url_pattern)




class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer





class LoginAPI(GenericAPIView):
    # permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            email = request.data['email']
            password = request.data['password']
            user1 = User.objects.get(email=email)
            if user1 is not None:
                try:
                    user = authenticate(request, email=user1.email, password=password)
                    if user is None:
                        return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
        if user:
            payload = {
                'id': user.id,
                'email': user.email,
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            UserToken.objects.create(user=user, token=jwt_token)
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                    "result": {'id': user.id,
                                            'name':user.name, 
                                            'email':user.email, 
                                            'token': jwt_token,
                                            }},
                                status=status.HTTP_200_OK)





class LogoutView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            token = Authenticate(self, request)
            token1 = token.decode("utf-8")
            try:
                user_token = UserToken.objects.get(user=request.user, token=token1)
                user_token.delete()
                logout(request)
            except:
                return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                      "Message": 'Already Logged Out.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"Status": status.HTTP_200_OK,
                                  "Message": "User Logged Out."},
                            status=status.HTTP_200_OK)
        except:
            return Response(data={"Status":status.HTTP_400_BAD_REQUEST,
                                    "Message":'Already Logged Out.'},
                            status=status.HTTP_400_BAD_REQUEST)




class ChangePasswordView(UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer





class ViewProfileAPI(GenericAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = ViewProfileSerializer
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = ViewProfileSerializer(user)
        return Response(serializer.data)    





class EditProfileAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=User.objects.get(id=request.user.id)
        serializer=EditProfileSerializer(user)
        return Response({'status':status.HTTP_100_CONTINUE,'message':'your profile','result':serializer.data})
    
    def patch(self,request):
        user = User.objects.get(id=request.user.id)
        serializer=EditProfileSerializer(instance = user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'your Profile update','result':serializer.data})
        else:
            return Response({'status':status.HTTP_404_NOT_FOUND,'message':'enter the valid data'})







class AddPostAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer 


    def post(self, request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response({'status':status.HTTP_201_CREATED,'message':'You Post Successfully','result':serializer.data})
        return Response({'status':status.HTTP_404_NOT_FOUND,'message':'please enter the valid data'})  




class EditPostAPI(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




class DeletePostAPI(GenericAPIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = PostSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')





class ViewPostAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewPostSerializer

    def get_queryset(self,request):
        return Post.objects.filter(user = request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data is not None:
            return Response(serializer.data)
        else:
            return Response(data={
                                    "Message":'Invalid User.'},
                            status=status.HTTP_400_BAD_REQUEST)






class ViewOnePostAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewPostSerializer

    def get_queryset(self,request,pk):
        return Post.objects.filter(user = request.user, id = pk )

    def list(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset(request,pk))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)      

        if serializer.data:
            return Response(serializer.data)
        return Response(data={"Message":'Invalid User.'},
                            status=status.HTTP_400_BAD_REQUEST)
        




class FolowAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        
        user = User.objects.get(id=pk)
        follower = request.user

        if Follower.objects.filter(user = user, follower= follower).first():
            delete_follower = Follower.objects.get(user = user, follower = follower)
            delete_follower.delete()
            return Response(data={"Status":status.HTTP_202_ACCEPTED,
                                    "Message":'Sucessfully Unfollow'},
                            status=status.HTTP_202_ACCEPTED)

        else:
            new_follower = Follower.objects.create(user = user, follower = follower)
            new_follower.save()
            return Response(data={"Status":status.HTTP_202_ACCEPTED,
                                    "Message":'Sucessfully Follow '},
                            status=status.HTTP_202_ACCEPTED)





class LikeAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]


    def post(self, request,pk):
        user = request.user
        post = Post.objects.get(id=pk)

        like_filter = LikePost.objects.filter(post = post, user = user).first()

        if like_filter == None:
            new_like = LikePost.objects.create(post = post, user = user)
            new_like.save()
            post.likes = post.likes+1
            post.save()
            return Response(data={"Status":status.HTTP_202_ACCEPTED,
                                    "Message":'Post Like '},
                            status=status.HTTP_202_ACCEPTED)
        else:
            like_filter.delete()
            post.likes = post.likes-1
            post.save()
            return Response(data={"Status":status.HTTP_202_ACCEPTED,
                                    "Message":'Post Unlike'},
                            status=status.HTTP_202_ACCEPTED)






class CommentAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        user = request.user
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = user, post=post )
            return Response(data={"Status":status.HTTP_202_ACCEPTED,
                                    "Message":'Commented On Post '},
                            status=status.HTTP_202_ACCEPTED)

        return Response(data={"Status":status.HTTP_400_BAD_REQUEST,
                                    "Message":'Invalid Data '},
                            status=status.HTTP_400_BAD_REQUEST)





class ViewCommentAPI(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ViewCommentSerializer

    def get_queryset(self,request,pk):
        uid = Post.objects.get(id =pk)
        return Comment.objects.filter(post__id = uid.id)

    def list(self, request, pk):
        queryset = self.filter_queryset(self.get_queryset(request,pk))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)      

        if serializer.data:
            return Response(serializer.data)
        return Response(data={"Message":'Invalid User.'},
                            status=status.HTTP_400_BAD_REQUEST)

