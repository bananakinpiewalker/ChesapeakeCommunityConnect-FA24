from django.core import serializers
from django.shortcuts import render, redirect
from account import views
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from account.models import Member
from .forms import *
from django.db.models import Q
import googlemaps
from datetime import datetime
from Janitor.forms import ForumRepForm
from django.shortcuts import get_object_or_404, render
from .models import Post, Forum
from django.core.paginator import Paginator
from django.template.loader import render_to_string



def viewMap(request):
    forums = Forum.objects.filter(visibility=1) #begin by fetching visible forums from database
    contQuery = request.GET.get("q") #get content and tag query from url
    tagQuery = request.GET.getlist("t")
    searchForm = SearchForumsForm(request.GET) #create a search form from url
    if contQuery: #filter the forums according to search queries if the search queries are nonempty
        forums = forums.filter(Q(title__icontains=contQuery) | Q(content__icontains=contQuery) )
    if tagQuery:
        for tag in tagQuery:
            forums=forums.filter(tags__pk=tag)
    widgets = serializers.serialize('json', forums) #serialize forums as JSON for google maps
    #print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets,
                                                      'searchForm' : searchForm,}) #render template



def forum_list(request):
    contQuery = request.GET.get("q")
    tagQuery = request.GET.getlist("t")
    form = SearchForumsForm(request.GET)
    forums = Forum.objects.filter(visibility=1)
    if contQuery:
        forums = forums.filter(Q(title__icontains=contQuery) | Q(content__icontains=contQuery) )
    if tagQuery:
        for tag in tagQuery:
            forums=forums.filter(tags__pk=tag)
    forums = forums.order_by("id")
    return render(request, "mapViewer/listForums.html", {"forumList" : forums,
                                                        "form" : form})

#this is practice of using url args and absolute URLs of a model. see models.py and urls.py to see how its working
def forum_detail(request, want):
    forum = get_object_or_404(Forum, id=want)
    msg=""
    hasReported=False
    if Forum.objects.filter(pk=want).exists():
        lookAt= Forum.objects.get(pk=want)
        files = Media.objects.filter(forum=lookAt)
        if request.method == 'POST':
            reporter = ForumRepForm(request.POST)
            hasReported = reporter.is_valid()
            if hasReported:
                reporter.save()
        else:
            reporter = ForumRepForm(initial={'forum':lookAt})
        posts = Post.objects.filter(forum=forum).order_by('author') #sorted by author
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        current_page = page_obj.number

        if lookAt.visibility>0 or request.session.get('rank',0)>1 or lookAt.author.pk==request.session.get('user',-1):
            
            if lookAt.visibility==0:
                msg="Your forum is currently pending approval and only visible to you."
            elif lookAt.visibility == -1:
                msg="Your forum has been denied for the following reason: {0}.\nTo resubmit, please create a new forum.".format(lookAt.description)
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    # Render each post using the postTemplate
                    post_html = [
                        render_to_string('mapViewer/postTemplate.html', {'post': post, 'forum': lookAt, 'page_obj': page_obj.number})
                        for post in page_obj.object_list
                    ]
                    
                    return JsonResponse({
                        'posts': post_html,
                        'has_next': page_obj.has_next()
                    })
                
                # Initial render for the HTML template

                return render(request, "mapViewer/viewForum.html", {"forum" : lookAt,
                                                                "form" : reporter,
                                                                "hasReported" : hasReported,
                                                                "files" : files,
                                                                "msg" : msg,
                                                                "posts" : page_obj, 
                                                                "page_number" : page_obj.number
                                                                })                
    return redirect(reverse("mapViewer:default"))

def post_detail(request, want, wants):
    if Forum.objects.filter(pk=want).exists():
        lookAt= Forum.objects.get(pk=want)
        lookAtPost= Post.objects.get(pk=wants)
        return render(request, "mapViewer/viewPost.html", {"forum" : lookAt,
                                                            "Post" : lookAtPost,})