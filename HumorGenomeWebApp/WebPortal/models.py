from django.db import models
from django.contrib import admin

class HumorContent(models.Model):
	url = models.CharField(max_length=150)
	title = models.CharField(max_length=150)
	rating = models.IntegerField()
	created = models.DateTimeField()

admin.site.register(HumorContent)
