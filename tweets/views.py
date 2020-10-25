from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Tweet   #should use relative imports when inside of an app

# Create your views here.
def home_view(request, *args, **kwargs):
    print(args, kwargs)
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request,"pages/home.html", context={}, status=200)

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
    except:
        data['message'] = "Not found"
        status = 404


    return JsonResponse(data, status=status)   # like json.dumps with content_type='application/json', not too familiar maybe check it out
    # return HttpResponse(f"<h1>Hello World \nTweet ID:{tweet_id} - {obj.content}</h1>")