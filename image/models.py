from django.db import models
from main.models import User
from django.core import exceptions as e

# Create your models here.

class Image(models.Model):

    TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('customized', 'Customized')
    )


    user            =models.ForeignKey(User, on_delete=models.CASCADE)
    # viewers         =models.CharField(max_length=10000, null=True, blank=True)
    image_url       =models.URLField(max_length=1000, help_text="Paste your image URL", unique=True)
    image_title     =models.CharField(max_length=200, help_text="Give your image title")
    image_type      =models.CharField(max_length=100, help_text="Image Type could be Personal or Customized", choices=TYPE_CHOICES)
    site_name       =models.CharField(max_length=100, help_text="The name of the site you copy image URL")
    your_name       =models.CharField(max_length=100, help_text="Your name on the site you copy image URL")
    approved        =models.BooleanField(default=False)
    viewed          =models.BooleanField(default=False)
    status          =models.CharField(max_length=100, blank=True, null=True, default="Pending")
    comment         =models.TextField("Comment On Your Image",max_length=1000, help_text="Describe your image and give good expression about us")
    date_published  =models.DateTimeField(auto_now_add=True)
    # date_viewed     =models.CharField(max_length=100, null=True, blank=True)
    # display_till    =models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return F"{self.image_title} by {self.your_name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('image:images')



class Viewer(models.Model):
    image = models.ForeignKey(Image, related_name="image", on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, related_name="viewer", on_delete=models.CASCADE)
    date_viewed = models.DateTimeField(auto_now_add=True)
    display_till = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return F"Image: {self.image} Viewer: {self.viewer}"

    class Meta:
        verbose_name_plural = "View Table"

class ImagePostReward(models.Model):
    premium_member_reward = models.DecimalField(max_digits=19, decimal_places=2, null = True)
    ordinary_member_reward = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Image Poster Reward"

    def __str__(self):
        return "Image post reward"

class ImageViewReward(models.Model):
    premium_viewer_reward = models.DecimalField(max_digits=19, decimal_places=2, null = True)
    ordinary_viewer_reward = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Image View Reward"

    def __str__(self):
        return "Image view reward"

class ImageViewCountDown(models.Model):
    seconds = models.PositiveIntegerField(null = True, blank=True, default=0)

    class Meta:
        verbose_name_plural = "Image View Count Down"

    def __str__(self):
        return str(self.seconds)

class ImageViewLimit(models.Model):
    limit = models.PositiveIntegerField(null = True, blank=True, default=0)

    class Meta:
        verbose_name_plural = "Image Daily View Limit"

    def __str__(self):
        return str(self.limit)
