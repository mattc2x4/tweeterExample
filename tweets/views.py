import random
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from .models import Tweet   #should use relative imports when inside of an app

from .forms import TweetForm


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request,"pages/home.html", context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
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

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)  #with or without data, sent through post method
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        #do other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) #status for created items
        if next_url !=None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})


def tweet_detail_view(request,tweet_id, *args, **kwargs):
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