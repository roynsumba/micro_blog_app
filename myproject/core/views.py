from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Tweet, Connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def home(request):
    tweet_list = Tweet.objects.order_by('-created_at')
    paginator = Paginator(tweet_list, 10)  # Show 10 tweets per page

    page = request.GET.get('page')
    tweets = paginator.get_page(page)

    context = {'tweets': tweets}
    return render(request, 'core/home.html', context)

def user_profile(request, username):
    user = User.objects.get(username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    is_following = request.user.is_authenticated and Connection.objects.filter(follower=request.user, followed=user).exists()
    context = {'user_profile': user, 'tweets': tweets, 'is_following': is_following}
    return render(request, 'core/user_profile.html', context)


@login_required
def create_tweet(request):
    if request.method == 'POST':
        content = request.POST['content']
        tweet = Tweet(user=request.user, content=content)
        tweet.save()
        return redirect('core:home')
    return render(request, 'core/create_tweet.html')

@login_required
def follow(request, user_id):
    followed_user = User.objects.get(id=user_id)
    connection = Connection(follower=request.user, followed=followed_user)
    connection.save()
    return redirect('home')

@login_required
def unfollow(request, user_id):
    followed_user = User.objects.get(id=user_id)
    connection = Connection.objects.get(follower=request.user, followed=followed_user)
    connection.delete()
    return redirect('home')
