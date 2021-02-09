from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Post (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length = 400)
    slug = models.SlugField(max_length = 20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.created.year,
         self.created.month,
          self.created.day,
           self.slug])