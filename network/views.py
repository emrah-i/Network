import uuid
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from functools import reduce
from operator import or_
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.middleware import csrf
from django.utils import timezone
from datetime import datetime
import json

from .models import User, Post, UserFollow, Comment

CATEGORY_CHOICES = [
    {'code': 'general', 'display': 'General Discussion', 'parent': 'General'},
    {'code': 'help', 'display': 'Help and Support', 'parent': 'General'},
    {'code': 'suggestions', 'display': 'Suggestions and Feedback', 'parent': 'General'},
    {'code': 'introductions', 'display': 'Introductions', 'parent': 'General'},
    {'code': 'offtopic', 'display': 'Off-Topic Discussion', 'parent': 'General'},

    {'code': 'news', 'display': 'News and Announcements', 'parent': 'Current Events'},
    {'code': 'education', 'display': 'Education and Learning', 'parent': 'Current Events'},
    {'code': 'health', 'display': 'Health and Wellness', 'parent': 'Current Events'},
    {'code': 'politics', 'display': 'Politics and Current Events', 'parent': 'Current Events'},
    {'code': 'business', 'display': 'Business and Entrepreneurship', 'parent': 'Current Events'},

    {'code': 'travel', 'display': 'Travel and Adventure', 'parent': 'Entertainment'},
    {'code': 'technology', 'display': 'Technology and Gadgets', 'parent': 'Entertainment'},
    {'code': 'entertainment', 'display': 'Entertainment and Media', 'parent': 'Entertainment'},
    {'code': 'sports', 'display': 'Sports and Fitness', 'parent': 'Entertainment'},
    {'code': 'food', 'display': 'Food and Cooking', 'parent': 'Entertainment'},

    {'code': 'arts', 'display': 'Arts and Creativity', 'parent': 'Art'},
    {'code': 'music', 'display': 'Music and Audio', 'parent': 'Art'},
    {'code': 'movies', 'display': 'Movies and TV Shows', 'parent': 'Art'},
    {'code': 'books', 'display': 'Books and Literature', 'parent': 'Art'},
    {'code': 'fashion', 'display': 'Fashion and Style', 'parent': 'Art'},
]

parents = ['General', 'Current Events', 'Entertainment', 'Art']

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def index(request):

    return render(request, "network/index.html")

def search_page(request): 

    return render(request, "network/search.html")
    
def search(request, query): 

    start = int(request.GET.get('start')) or 0
    end = start + 9
    sort = request.GET.get('sort')

    if query is None:
        return

    query_list = query.split(' ')

    word_queries = []

    for word in query_list:
        word_query = (
            Q(title__icontains=word) |
            Q(text__icontains=word) |
            Q(user__username__icontains=word) |
            Q(comment_post__text__icontains=word)
        )
        word_queries.append(word_query)

    combined_q = Q()
    for word_query in word_queries:
        combined_q &= word_query

    filtered_posts = Post.objects.filter(combined_q).distinct()

    post_ids = []
    for post in filtered_posts:
        post_ids.append(post.post)

    posts_list = Post.objects.filter(post__in=post_ids)
    posts_full = posts_list.annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count',  'upload_time', 'category')

    for post in posts_full:
        unique_users = []
        comments = Comment.objects.filter(post=post['post'])
        post['comment_count'] = len(comments)
        
        for comment in comments:
            if comment.user not in unique_users:
                unique_users.append(comment.user)
                
        post["unique_users"] = len(unique_users)

    if sort == "new_old":
        posts = sorted(posts_full, key=lambda post: post['upload_time'], reverse=True)
    elif sort == "old_new":
        posts = sorted(posts_full, key=lambda post: post['upload_time'])
    elif sort == "most_likes":
        posts = sorted(posts_full, key=lambda post: post['like_count'], reverse=True)
    elif sort == "least_likes":
        posts = sorted(posts_full, key=lambda post: post['like_count'])
    elif sort == "most_comments":
        posts = sorted(posts_full, key=lambda post: post['comment_count'], reverse=True)
    elif sort == "least_comments":
        posts = sorted(posts_full, key=lambda post: post['comment_count'])
    elif sort == "rel":
        posts = sorted(posts_full, key=lambda post: get_relavance_score(post, query), reverse=True)
            
    data = []
    for post in posts[start:end + 1]:
        post["upload_time"] = post["upload_time"].strftime("%B %d %Y, %I:%M %p")
        data.append(post)

    return JsonResponse(data, safe=False)

def get_relavance_score(post, query):

    all_words = query.split(' ')
    title_count = text_count = username_count = comment_count = 0

    for word in all_words:
        title_count += post['title'].lower().count(word.lower())
        text_count += post['text'].lower().count(word.lower())
        username_count += post['user__username'].lower().count(word.lower())
        
    comments = Comment.objects.filter(post=post['post'])

    for comment in comments:
        if comment.text is not None:
            comment_count += comment.text.lower().count(query.lower())
    
    return title_count + text_count + username_count + comment_count

def posts(request):

    if request.method == "POST":
        
        user = User.objects.get(username = request.user.username)
        text = request.POST.get("text")
        title = request.POST.get("title")
        category = request.POST.get("category")

        newPost = Post.objects.create(user=user, text=text, title=title, category=category)
        newPost.save()

        return HttpResponseRedirect(reverse('index'))

    else:
        start = int(request.GET.get('start') or 0)
        end = start + 9
        sort = request.GET.get('sort')

        if sort == "new_old":
            posts = Post.objects.all().annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count',  'upload_time', 'category').order_by('-upload_time')
        elif sort == "old_new":
            posts = Post.objects.all().annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('upload_time')
        elif sort == "most_likes":
            posts = Post.objects.all().annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-like_count')
        elif sort == "least_likes":
            posts = Post.objects.all().annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('like_count')
        elif sort == "most_comments":
            posts = Post.objects.all().annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-comment_count')
        elif sort == "least_comments":
            posts = Post.objects.all().annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('comment_count')

        data = []
        for post in posts[start:end + 1]:
            post["upload_time"] = post["upload_time"].strftime("%B %d %Y, %I:%M %p")
            unique_users = []
            comments = Comment.objects.filter(post=post['post'])

            for comment in comments:
                if comment.user not in unique_users:
                    unique_users.append(comment.user)
                    
            post["unique_users"] = len(unique_users)
            data.append(post)

        return JsonResponse(list(data), safe=False)
    
def post(request, post_id): 

    if request.method == "POST":
        
        text = request.POST.get('comment_text')
        user = request.user

        post = Post.objects.get(pk=post_id)
        new_comment = Comment.objects.create(user=user, post=post, text=text)
        new_comment.save()

        return HttpResponseRedirect(reverse('post', args=(post_id, )))

    else:
        post = Post.objects.filter(pk=post_id).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category')
        comment_post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=comment_post, parent_node=None).order_by('upload_time')
        level = 40 

        for choice in CATEGORY_CHOICES:
            if choice['code'] == post[0]['category']:
                category = choice['display']

        post = {
            'id': post[0]['post'],
            'title': post[0]['title'],
            'text': post[0]['text'],
            'user': post[0]['user'],
            'username': post[0]['user__username'],
            'likes': post[0]['like_count'],
            'comments': post[0]['comment_count'],
            'category': category,
            'upload_time': post[0]['upload_time'],
        }

        return render(request, "network/post.html", {
            'post': post,
            'comments': comments,
            'level': level
        })

@login_required
def get_csrf_token(request):
    csrf_token = csrf.get_token(request)

    if request.user.is_authenticated:
        username = request.user.username
    
    return JsonResponse({'csrf_token': csrf_token, 'username': username})

def account(request, username):

    user = User.objects.get(username=username)

    user_following = UserFollow.objects.filter(user = user)
    user_followers = UserFollow.objects.filter(is_now_following = user)

    user_info  = {
            'id': user.id,
            'username': user.username,
            'following': len(user_following),
            'followers': len(user_followers),
            'avatar': user.avatar,
            'bio': user.bio,
        }

    following = UserFollow.objects.filter(user = user).values('is_now_following')
    followers = UserFollow.objects.filter(is_now_following = user).values('user')

    following_users = []
    for follow in following:
        current_user = User.objects.get(id = follow['is_now_following'])

        following_users.append(
            {
                'username': current_user.username,
                'id': current_user.id
            }
        )

    follower_users = []
    for follow in followers:
        current_user = User.objects.get(id = follow['user'])

        follower_users.append(
            {
                'username': current_user.username,
                'id': current_user.id
            }
        )


    current_user_following = False
    
    for usf in follower_users:
        if request.user.username == usf['username']:
            current_user_following = True
            break

    return render(request, "network/profile.html", {
        'user_info': user_info, 
        'following_users': following_users,
        'follower_users': follower_users,
        "current_user_following": current_user_following
    })

def profile(request, username):

    # when get requests come into this page, it should load the userpage
    # another route must be the get route when you can get the data
    
    user = User.objects.get(username=username)
    sort = request.GET.get('sort')
    print(request.GET.get('start'))
    start =int(0 or request.GET.get('start'))
    end = start + 9

    if sort == "new_old":
        posts = Post.objects.filter(user = user).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-upload_time')
    elif sort == "old_new":
        posts = Post.objects.filter(user = user).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('upload_time')
    elif sort == "most_likes":
        posts = Post.objects.filter(user = user).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-like_count')
    elif sort == "least_likes":
        posts = Post.objects.filter(user = user).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('like_count')
    elif sort == "most_comments":
        posts = Post.objects.filter(user = user).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-comment_count')
    elif sort == "least_comments":
        posts = Post.objects.filter(user = user).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('comment_count')

    data = []
         
    for post in posts[start:end + 1]:
        post["upload_time"] = post["upload_time"].strftime("%B %d %Y, %I:%M %p")
        unique_users = []
        comments = Comment.objects.filter(post=post['post'])

        for comment in comments:
            if comment.user not in unique_users:
                unique_users.append(comment.user)
                
        post["unique_users"] = len(unique_users)
        data.append(post)

    return JsonResponse(list(data), safe=False)

@login_required
def edit_profile(request):

    user = User.objects.get(pk=request.user.id)

    if request.method == "POST":

        bio = request.POST.get('bio')

        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            extension = avatar.name.split('.')[-1]
            random_name = f'{uuid.uuid4().hex}.{extension}'
            avatar.name = random_name
            user.avatar = avatar
        
        user.bio = bio
        user.save()

        last_page = request.META.get('HTTP_REFERER')
        return redirect(last_page)

    else:

        return render(request, "network/edit_profile.html", {
            'avatar': user.avatar,
            'bio': user.bio
        })

@login_required
def following(request):

    user = request.user.id
    following = UserFollow.objects.filter(user = user).values('is_now_following')

    following_users = []
    for follow in following:
        following_users.append(follow['is_now_following'])

    following = []
    for user in following_users:
        following.append(User.objects.get(pk=user))

    return render(request, 'network/following.html', {
        'following_users': following
    })

@login_required
def following_posts(request, start, sort):

    user = request.user.id
    start_post = start
    end = start_post + 9

    following = UserFollow.objects.filter(user = user).values('is_now_following')

    following_users = []
    for follow in following:
        following_users.append(follow['is_now_following'])

    following = []
    for user in following_users:
        following.append(User.objects.get(pk=user))

    if sort == "new_old":
        following_posts = Post.objects.filter(user__in = following).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-upload_time')
    elif sort == "old_new":
        following_posts = Post.objects.filter(user__in = following).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('upload_time')
    elif sort == "most_likes":
        following_posts = Post.objects.filter(user__in = following).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-like_count')
    elif sort == "least_likes":
        following_posts = Post.objects.filter(user__in = following).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('like_count')
    elif sort == "most_comments":
        following_posts = Post.objects.filter(user__in = following).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-comment_count')
    elif sort == "least_comments":
        following_posts = Post.objects.filter(user__in = following).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('comment_count')

    data = []
    for post in following_posts[start_post:end + 1]:
        post["upload_time"] = post["upload_time"].strftime("%B %d %Y, %I:%M %p")
        unique_users = []
        comments = Comment.objects.filter(post=post['post'])

        for comment in comments:
            if comment.user not in unique_users:
                unique_users.append(comment.user)
                
        post["unique_users"] = len(unique_users)
        data.append(post)

    return JsonResponse(list(data), safe=False)

@csrf_exempt
@login_required
def edit(request, post_id):

    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":

        data = json.loads(request.body)
        if data.get("text") is not None:
            post.text = data["text"]
        if data.get("title") is not None:
            post.title = data["title"]
        if data.get("category") is not None:
            post.category = data["category"]
        post.upload_time = str(timezone.now())
        post.save()
        return HttpResponse(status=204)
    
    elif request.method == "DELETE":

        post.delete()
    
    else:   

        data = {
            'post': post.post,
            'text': post.text,
            'title': post.title,
            'category_display': post.get_category_display(),
            'category': post.category,
        }

        return JsonResponse(data, safe=False)
    
@csrf_exempt
@login_required
def edit_comment(request, comment_id):

    try:
        comment = Comment.objects.get(user=request.user, pk=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found."}, status=404)
    
    if request.method == "PUT":

        data = json.loads(request.body)
        if data.get("text") is not None and data["text"] is not "[DELETED]":
            comment.text = data["text"]
        comment.upload_time = str(timezone.now())
        comment.save()
        return HttpResponse(status=204)
    
    elif request.method == "DELETE":
        comment.delete()
    
    else:
        
        data = {
            'text': comment.text,
        }
        return JsonResponse(data, safe=False)
    
@csrf_exempt
@login_required
def unfollow(request, user_uf): 

    try:
        user = request.user.id
        following = UserFollow.objects.get(user=user, is_now_following=user_uf)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Entry not found."}, status=404)

    following.delete()

@csrf_exempt
@login_required
def remove(request, user_uf): 

    try:
        user = request.user.id
        following = UserFollow.objects.get(user=user_uf, is_now_following=user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Entry not found."}, status=404)

    following.delete()

@csrf_exempt
@login_required
def follow(request, user_f): 

    try:
        user = request.user
        follow_user = User.objects.get(id=user_f)
    except User.DoesNotExist:
        return JsonResponse({"error": "Entry not found."}, status=404)

    follow = UserFollow.objects.create(user=user, is_now_following=follow_user)
    follow.save()

@csrf_exempt
@login_required
def like(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    user = request.user
    
    if request.method == "POST":

        post.likes.add(user)
        return HttpResponse(status=204)

    elif request.method == "PUT": 

        post.likes.remove(user)
        return HttpResponse(status=204)

    else:
        for liker in post.likes.all():
            if user == liker:
                data = True
                return JsonResponse(data, safe=False)
        
        data = False
        return JsonResponse(data, safe=False)

@csrf_exempt  
@login_required
def reply(request, commentid):
    
    reply_text = request.POST.get('reply_text')
    postid = request.POST.get('postid')
    parent_node = Comment.objects.get(pk=commentid)
    parent_post = Post.objects.get(pk=postid)
    user = request.user

    new_reply = Comment.objects.create(text=reply_text, user=user, parent_node=parent_node, post=parent_post)
    new_reply.save()

    return HttpResponseRedirect(reverse('post', args=(postid, )))

def categories(request):

    for category in CATEGORY_CHOICES:
        post_count = Post.objects.filter(category=category['code'])
        comment_count = Comment.objects.filter(post__category=category['code'])
        category['post_count'] = len(post_count)
        category['comment_count'] = len(comment_count)

    return render(request, 'network/categories.html', {
        'categories': CATEGORY_CHOICES,
        'parents': parents
    })

def category(request, category):
        
        categorydisplay = {
            'code': category
        }
        
        for choice in CATEGORY_CHOICES:
            if choice['code'] == category:
                categorydisplay['display'] = choice['display']
        
        return render(request, 'network/category.html', {
            'category': categorydisplay
        })

def category_posts(request, category, start, sort):
    
    start_post = start
    end = start_post + 9

    if sort == "new_old":
        posts = Post.objects.filter(category=category).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-upload_time')
    elif sort == "old_new":
        posts = Post.objects.filter(category=category).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('upload_time')
    elif sort == "most_likes":
        posts = Post.objects.filter(category=category).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-like_count')
    elif sort == "least_likes":
        posts = Post.objects.filter(category=category).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('like_count')
    elif sort == "most_comments":
        posts = Post.objects.filter(category=category).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('-comment_count')
    elif sort == "least_comments":
        posts = Post.objects.filter(category=category).annotate(like_count=Count('likes'), comment_count=Count('comment_post')).values('post', 'title', 'text','user', 'user__username', 'like_count', 'comment_count', 'upload_time', 'category').order_by('comment_count')

    data = []
    for post in posts[start_post:end + 1]:
        post["upload_time"] = post["upload_time"].strftime("%B %d %Y, %I:%M %p")
        unique_users = []
        comments = Comment.objects.filter(post=post['post'])

        for comment in comments:
            if comment.user not in unique_users:
                unique_users.append(comment.user)
                
        post["unique_users"] = len(unique_users)
        data.append(post)

    return JsonResponse(data, safe=False)

def auth(request):

    if request.user.is_authenticated: 
        user = True
    else:
        user = False
    
    return JsonResponse(user, safe=False)
    
@csrf_exempt
@login_required 
def comment(request, commentid): 

    try:
        comment = Comment.objects.get(pk=commentid)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found."}, status=404)

    data = json.loads(request.body)
    text = data.get('text')
    comment.text = text
    comment.save()
    return HttpResponse(status=204)

