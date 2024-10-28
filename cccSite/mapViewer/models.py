from django.db import models
from account.models import Member
from django.urls import reverse
from uuid import uuid4
import magic


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    def __str__(self):
        return self.name

# this will be the ideal forum model. we would serialize this to widgets using djangos JSON serialize functionality on the specific fields
class Forum(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    author = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name="forums", db_constraint=False)
    
    description = models.TextField()
    geoCode = models.JSONField()
    tags = models.ManyToManyField(Tag, related_name="forums", blank=True)
    
    
    visible_options = { 
        (-1,"denied"),
        (0, "pending"),
        (1 , "visible"),
    }
    visibility = models.SmallIntegerField(default=0, choices=visible_options)
    
    
    associated_choices = [
        ("associated", "I am associated with the group providing this solution"),
        ("not-associated", "I am not associated with the group providing this solution")
    ]
    associated = models.CharField(choices=associated_choices, max_length=150)
    
    private_public_choices = [
        ("public", "Public (Anyone can view and add Posts)"),
        ("private", "Private (Only invited Contributors can view and add Posts)")
    ]
    private_public = models.CharField(choices=private_public_choices, max_length=80)
    
    contributors = models.ManyToManyField(Member, related_name="contributed_forums", blank=True)
    
    def __str__(self):
        return self.title + " by " + str(self.author)
    @property
    def get_absolute_url(self):
        return reverse("mapViewer:forum_detail", args=[str(self.pk)])
    @property
    def get_admin_url(self):
        return reverse("Janitor:forumReview", args=[str(self.pk)])
    
    #https://forum.djangoproject.com/t/url-template-tag-get-absolute-url-and-views/21249
    #https://levelup.gitconnected.com/django-quick-tips-get-absolute-url-1c22321f806b

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    author = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name="posts", db_constraint=False)
    
    forum = models.ForeignKey(Forum, null=True, on_delete=models.SET_NULL, related_name="posts", db_constraint=False)
    

class Comment(models.Model):
    content = models.TextField()
    
    author = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name="comments", db_constraint=False)
    
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL, related_name="comments", db_constraint=False)
    
class Reply(Comment):
    
    parent = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL, related_name="children", db_constraint=False)
    # It's not really a recipient. It's just the Reply object this Reply object is replying to. I can't think of a better word.
    recipient = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="replies", db_constraint=False)
    
    
    

def media_directory(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / forums / <forum.pk> / <pk>.<ext>
    ext = filename.split('.')[-1]
    filename="{0}.".format(uuid4().hex)+ext
    return 'forums/{0}/{1}'.format(instance.forum.pk, filename) 

class Media(models.Model):
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    
    format_options = { 
        (0, "image"),
        (1, "video"),
        (2 , "audio"),
    }
    format = models.SmallIntegerField(default=0, choices=format_options)
    file = models.FileField(upload_to=media_directory)
    def get_format(self):
        filetype = magic.from_buffer(self.file.read(), mime=True).split('/')[0]
        match filetype:
            case "image":
                return 0
            case "video":
                return 1
            case "audio":
                return 2
            
