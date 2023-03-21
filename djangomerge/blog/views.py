from django.contrib.auth.forms import AuthenticationForm
# from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, User, Comments
from .forms import PostForm, UserForm, LoginForm, CommentForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})


def category(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    category = posts.category
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)

def tags(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    tags = posts.tags
    posts = Post.objects.filter(tags=tags)
    context = {
        'tags': tags,
        'posts': posts,
    }
    return render(request, 'blog/tags.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comment = Comments.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                parent = request.POST.get('comment_id', None)
                parent = Comments.objects.filter(id=parent).last()
            except:
                parent = None
            print(parent, '************')
            comment = form.save(commit=False)
            comment.post = post
            comment.parent = parent
            comment.save()
        return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comment})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # post.tags.set(form.cleaned_data.get('tags'))
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.tags.set(form.cleaned_data.get('tags'))
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def signup_request(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print(form)
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('blog:post_list')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserForm()
    return render(request, "blog/signup.html", {"form": form})


def login_request(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("blog:post_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = LoginForm()
    return render(request=request, template_name="blog/login.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("blog:login")


@login_required
def profile_request(request):
    user = get_object_or_404(User, pk=request.user.id)
    return render(request=request, template_name="blog/profile.html", context={"user": user})


# @login_required
# def edit_request(request):

#  if request.method == 'POST':
#         edit = edit_request(request.POST, instance=request.edit)

# #         if edit.is_valid() :
# #             edit.save()
# #             messages.success(request, 'Your profile is Edit successfully')
# #             return redirect(to='edit-profile')
# #  else:
# #         edit = edit (instance=request.edit)

# # 	# return render(request, 'blog/edit_profile.html', {'user_form': edit_request})


@login_required
def edit_profile(request):
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            print(form)
            user = form.save()
            login(request, user)
            messages.success(request, "Profile updated successful.")
            return redirect('blog:post_list')
        messages.error(request, "Something went wrong. Invalid information.")
    else:
        form = UserForm(instance=request.user)
    return render(request, "blog/editprofile.html", {"form": form})


# def postComment(request):
#     if request.method == "POST":
#         comment=request.POST.get('comment')
#         user=request.user
#         postSno =request.POST.get('postSno')
#         post= Post.objects.get(sno=postSno)
#         parentSno= request.POST.get('parentSno')
#         if parentSno=="":
#             comment=BlogComment(comment= comment, user=user, post=post)
#             comment.save()
#             messages.success(request, "Your comment has been posted successfully")
#         else:
#             parent= BlogComment.objects.get(sno=parentSno)
#             comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
#             comment.save()
#             messages.success(request, "Your reply has been posted successfully")

#            return redirect(f"/blog/ {"form":form}")


# def tag(request, slug):
# 	tag = get_object_or_404(Tag, slug=slug)
# 	# Filter posts by tag name
# 	posts = Post.objects.filter(tags=tag)
# 	context = {
# 		'tags':tag,
# 		'posts':posts,
# 	}
# 	return render(request, 'profile.html', context)
