from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image



# Create your models here.
class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='post/%Y%m%d/', blank=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    topic = TaggableManager(blank=True)
    total_views = models.IntegerField(default=0)
    column = models.ForeignKey(
                                ArticleColumn,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name='article'
    )

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jimblog:detail', args=[self.id])

    def save(self, *args, **kwargs):
        post = super(Article, self).save(*args, **kwargs)

        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x =400
            new_y = int(new_x * (y/x))
            resiezed_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resiezed_image.save(self.avatar.path)

        return post



