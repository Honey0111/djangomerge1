from django.contrib import admin
from django.urls import path, include
# from blog import api
# from . import api
from django.contrib import auth

from django.urls import include, path
from rest_framework import routers
from blog.api import UserViewSet,LoginViewSet,PostViewSet,CategoryViewSet, TagsViewSet, CommentsViewSet, EditProfileViewSet

router = routers.DefaultRouter()
# user API 
router.register(r'users', UserViewSet)
router.register(r'user_list', UserViewSet)
router.register(r'user_detail', UserViewSet)


# PostAPI
router.register(r'posts', PostViewSet)
# CategoryAPI
router.register(r'category', CategoryViewSet)
# Tags API
router.register(r'tags', TagsViewSet)
# Comments API
router.register(r'comments', CommentsViewSet)
# Profile API
router.register(r'profiles', EditProfileViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
    # path('logoutall/', LogoutAllViewSet.as_view(), name='logoutall'),

]