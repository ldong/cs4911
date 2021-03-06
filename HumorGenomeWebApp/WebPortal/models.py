from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import datetime

class Rating(models.Model):
	rating = models.IntegerField();
	user = models.ForeignKey(User);
	humor = models.ForeignKey('HumorContent');
	flag = models.BooleanField(default=False);
	favorite = models.BooleanField(default=False);

class HumorContent(models.Model):
	url = models.CharField(max_length=150, default="")
	contentType = models.CharField(max_length=10)
	message = models.TextField(default="")
	title = models.CharField(max_length=150)
	avgRating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	numRatings = models.IntegerField(default=0)
	created = models.DateTimeField(default=datetime.now)
	numFlags = models.IntegerField(default=0)
	flagRatio = models.DecimalField(max_digits=4, decimal_places=2, default=0)
	createdBy = models.ForeignKey(User);

class HumorContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'avgRating', 'numRatings', 'created')

class RatingAdmin(admin.ModelAdmin):
	list_display = ('rating', 'user', 'humor', 'flag')


admin.site.register(Rating, RatingAdmin)
admin.site.register(HumorContent, HumorContentAdmin)
