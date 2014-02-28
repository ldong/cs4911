from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Rating(models.Model):
	rating = models.IntegerField();
	user = models.ForeignKey(User);
	humor = models.ForeignKey('HumorContent');

class HumorContent(models.Model):
	url = models.CharField(max_length=150)
	title = models.CharField(max_length=150)
	avgRating = models.DecimalField(max_digits=3, decimal_places=1)
	numRatings = models.IntegerField()
	created = models.DateTimeField()

class HumorContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'avgRating', 'numRatings', 'created')

admin.site.register(HumorContent, HumorContentAdmin)
