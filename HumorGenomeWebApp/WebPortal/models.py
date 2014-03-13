from django.db import models
from django.db.models.signals import post_save
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
