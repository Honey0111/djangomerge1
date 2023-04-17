from rest_framework import viewsets,status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import User,Post,Category,Tags, Comments
from django.contrib.auth import get_user_model, authenticate

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .serializers import SignupSerializer , LoginSerializer,PostSerializer,CategorySerializer, TagsSerializer, CommentsSerializer,EditProfileSerializer


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'city': user.city})
    

class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
            'user_id': user.pk,
            'email': user.email})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data['title']
        if Post.objects.filter(title=title).exists():
            return Response({'error': 'Post with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data['title']
        if Tags.objects.filter(title=title).exists():
            return Response({'error': 'Tag with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class EditProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EditProfileSerializer











