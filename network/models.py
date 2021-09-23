from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timezone
from datetime import timedelta
from django.forms import ModelForm
from django import forms

class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    user_name = models.CharField(max_length=25, default="string", null=True, blank=True)
    post = models.CharField(max_length=1440, default='', null=True, blank=True)
    time_added = models.DateTimeField(max_length=64, default=datetime.now(timezone.utc))
    likes = models.IntegerField(default="0")

    def serialize(self):
        return {
            "id"  : self.id, 
            "user": self.user,
            "user_name": self.user_name,
            "post": self.post,
            "timestamp": self.time_added.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }
        
class EditForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(Post, self).__init__(*args, **kwargs)
    #     ## add a "form-control" class to each form input
    #     ## for enabling bootstrap
    #     for name in self.fields.keys():
    #         self.fields[name].widget.attrs.update({
    #             'class': 'form-control',
    #         })

    class Meta:
        model = Post
        fields = ["id", "post"]      


class Profile(models.Model): #extends the user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    # followers = models.IntegerField(default="0")

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='follower')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='followee')
    class Meta:
        unique_together = ["follower", "followee"]

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="liker")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True)
    # class Meta:
    #     unique_together = (('post', 'liker'),)
    def serialize(self):
        return {
            "liker"  : self.liker, 
            "post": self.post,
        }

    # def __str__(self):
    #     return f"{self.post} : {self.user}"


