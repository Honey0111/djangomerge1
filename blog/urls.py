from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [ 
    path("signup", views.signup_request, name="signup"),
    path("login", views.login_request, name="login"),
    path('post/new/', views.post_new, name='post_new'),

    path('', views.post_list, name='post_list'),
    path('category/<str:slug>', views.category, name='category'),
    path('tags/<str:slug>', views.tags, name='tags'),
    path('profile/', views.profile_request, name='profile'),
    path("edit_profile", views.edit_profile, name="edit-profile"),
    path('post/<str:slug>', views.post_detail, name='post_detail'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path("post/new/", views.post_new, name="post_new"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("comments/", views.post_detail, name= "comments"),
]
