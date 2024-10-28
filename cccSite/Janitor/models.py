from django.db import models
from mapViewer.models import Forum
from account.models import Member

# Create your models here.
class ForumReport(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, db_constraint=False)
    reason = models.TextField()

class UserReport(models.Model):
    account = models.ForeignKey(Member, on_delete=models.CASCADE, db_constraint=False)
    reason = models.TextField()


    