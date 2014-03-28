from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import datetime

class Rating(models.Model):
	rating = models.IntegerField(default=0);
	user = models.ForeignKey(User);
	humor = models.ForeignKey('HumorContent');
	flag = models.BooleanField(default=False);

class HumorContent(models.Model):
	url = models.CharField(max_length=150)
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

## User models ##

class RegularUser(models.Model):
	user		= models.OneToOneField(User)
	name		= models.CharField(max_length=100)
	birthday	= models.DateField()

	def __unicode__(self):
		return self.name # This returns the name of User object

# create our user object to attach to our RegularUser object
#def create_regularuser_callback(sender, instance, **kwargs):
#	regularuser, new = RegularUser.objects.get_or_create(user=instance)
#post_save.connect(create_regularuser_callback, User)
