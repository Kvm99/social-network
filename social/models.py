from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_action = models.CharField(max_length=200, blank=True)


class Post(models.Model):
    user = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )

    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    likes_amount = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['likes_amount']

    def __str__(self):
        return '%d: %s' % (self.likes_amount, self.text)


class Like(models.Model):
    id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(
        User,
        related_name='users',
        on_delete=models.CASCADE
    )
    post_id = models.ForeignKey(
        Post,
        related_name='posts',
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
