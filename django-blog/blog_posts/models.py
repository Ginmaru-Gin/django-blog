from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    header = models.CharField(max_length=80, default="")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()


    def __str__(self):
        return f"Post \"{self.header}\" from {self.author}"
    

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"Comment for \"{self.post.header}\" from {self.author}"
