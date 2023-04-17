from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *
from blog.models import User

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return data
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = fields = ('id','title', 'text', 'category', 'tags','featured_image','thumbnail_image' ,'author')


    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        fields = ('id','title')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        # fields = '__all__'
        fields = ('id','title')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        # fields = ('id','title')



class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        # fields = ['username', 'first_name', 'last_name', 'email']

        # fields = ('id','title')