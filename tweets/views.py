import random
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from rest_framework.serializers import Serializer


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from .models import Tweet   #should use relative imports when inside of an app
from .forms import TweetForm
from .serializers import (
    TweetSerializer,
    TweetActionSerializer,
    TweetCreateSerializer,
)


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request,"pages/home.html", context={}, status=201)


@api_view(['POST'])  #client sends http request POST
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request,tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs:
        return Response({}, 404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['GET','DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    doesnt have to be owner of tweet to do
    '''
    print(request.POST,request.data)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        parent_content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        if not qs.exists():
            return Response({"message": "You cannot like this tweet"}, status=401)
        obj = qs.first()
        if action =="like" and request.user not in obj.likes.all():
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike" or (request.user in obj.likes.all() and action != "retweet"):
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action=="retweet":
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=obj,
                content=parent_content,
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)


    return Response({"message": "Tweet Action Performed"}, status=200)


    


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Consume :0
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response":tweets_list,
    }
    return JsonResponse(data)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)  #with or without data, sent through post method
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user  #anon user = none, but we don't allow user=NULL
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) #status for created items
        if next_url !=None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors,status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_detail_view_pure_django(request,tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume :0
    return json data
    """
    print(args, kwargs)
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
         
        #data['image'] = obj.image
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)   # like json.dumps with content_type='application/json', not too familiar maybe check it out
    # return HttpResponse(f"<h1>Hello World \nTweet ID:{tweet_id} - {obj.content}</h1>")