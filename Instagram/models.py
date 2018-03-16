from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path_to_img = models.FileField()
    amount_of_comments = models.IntegerField(default=0, editable=False)
    amount_of_likes = models.IntegerField(default=0, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User: {}, Name: {}'.format(self.user.username, self.path_to_img)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User: {}, Img: {}, Comment: {}'.format(self.user.username, self.img, self.comment[:20])

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return 'User: {}, Img: {}'.format(self.user.username, self.img)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return 'Follower: {}, Following: {}'.format(self.follower.username, self.follower.username)
