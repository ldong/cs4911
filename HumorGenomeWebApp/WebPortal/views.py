from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from WebPortal.models import HumorContent, Rating, RegularUser
from WebPortal.forms import RegistrationForm

def archive(request):
	humorContents = HumorContent.objects.order_by('id');
	mostRecent = humorContents[len(humorContents) - 1];
	c = RequestContext(request, { 'humorContent': mostRecent });

	if(request.user.is_authenticated()):
		curUser = request.user;
		myRating = Rating.objects.filter(user=curUser).filter(humor=mostRecent);
		if(len(myRating) > 0):
			myRating = myRating[0];
			c.update({'rating': myRating.rating});
			c.update({'flag': myRating.flag});

	t = loader.get_template("archive.html")
	#c.update(csrf(request))
	return HttpResponse(t.render(c))

def logout(request):
    auth_logout(request)
    humorContents = HumorContent.objects.order_by('id');
    mostRecent = humorContents[len(humorContents) - 1];
    c = RequestContext(request, { 'humorContent': mostRecent });
    t = loader.get_template("archive.html")
    return HttpResponse(t.render(c))

def login(request):
	t = loader.get_template("archive.html")
	humorContents = HumorContent.objects.order_by('id');
	mostRecent = humorContents[len(humorContents) - 1];
	username = request.POST['username'];
	password = request.POST['password'];
	user = authenticate(username=username, password=password)
	c = RequestContext(request, { 'humorContent': mostRecent });
	if user is not None:
		if user.is_active:
			auth_login(request, user) #todo - bad login logic later

	if(request.user.is_authenticated()):
		myRating = Rating.objects.filter(user=user).filter(humor=mostRecent);
		if(len(myRating) > 0):
			myRating = myRating[0];
			c.update({'rating': myRating.rating});
			c.update({'flag': myRating.flag});

	return HttpResponse(t.render(c))

def flagContent(request):
	if(request.GET.get('id') and request.user):
		myId = int(request.GET.get('id'));
		curUser = request.user;
		humorContent = HumorContent.objects.get(pk=myId);
		myRating = Rating.objects.filter(user=curUser).filter(humor=humorContent);
		
		if(len(myRating) > 0): #rating exists
			myRating = myRating[0];
			myRating.flag = not myRating.flag;

			if(myRating.flag):
				humorContent.numFlags += 1;
			else:
				humorContent.numFlags -= 1;
			
			myRating.save();
		else: #new rating
			print 'hey1'
			myRating = Rating();
			print 'hey1'
			myRating.user = curUser;
			myRating.humor = humorContent;
			humorContent.numFlags = humorContent.numFlags + 1;
			myRating.save();
			print 'hey'

		if(humorContent.numRatings != 0):
			humorContent.flagRatio = (humorContent.numFlags)/humorContent.numRatings;
		else:
			humorContent.flagRatio = 99;
		humorContent.save();
		return HttpResponse("OKAY");
	return HttpResponse("BAD");

def submitRating(request):
	if(request.GET.get('id') and request.user):
		myId = int(request.GET.get('id'));
		humorContent = HumorContent.objects.get(pk=myId);
		newRating = int(request.GET.get('rating'));
		weight = int(humorContent.numRatings);
		oldAverage = float(humorContent.avgRating);
		newAverage = 0;
		curUser = request.user;
		myRating = Rating.objects.filter(user=curUser).filter(humor=humorContent);

		if(len(myRating) > 0): #updating existing rating
			myRating = myRating[0];
			oldRating = myRating.rating;
			myRating.rating = newRating;

			if(oldRating is not None):
				newAverage = ((oldAverage * weight) + newRating - oldRating) / (humorContent.numRatings);
			else:
				newAverage = ((oldAverage * weight) + newRating) / (humorContent.numRatings + 1);
				humorContent.numRatings = humorContent.numRatings + 1;

			myRating.save();
		else: #first rating from this user
			myRating = Rating(rating=newRating);
			myRating.user = curUser;
			myRating.humor = humorContent;
			newAverage = ((oldAverage * weight) + newRating) / (humorContent.numRatings + 1);
			humorContent.numRatings = humorContent.numRatings + 1;
			myRating.save();

		humorContent.avgRating = newAverage;
		humorContent.save();
		result= { 'rating': newRating, 'avgRating': newAverage, 'numRatings': humorContent.numRatings };
		return HttpResponse(simplejson.dumps(result), content_type='application/json');
	return HttpResonse("BAD");

def getNextHumor(request):
	if(request.GET.get('id')):
		humorContents = HumorContent.objects.order_by('id');
		index = 0;

		for i, j in enumerate(humorContents):
			if j.id == int(request.GET.get('id')):
				index = i;

		nextIndex = index + 1;
		nextIndex = ((nextIndex) % len(humorContents));
		desiredHumor = humorContents[nextIndex];
		result = {}
		result.update({'id': desiredHumor.id});
		result.update({'url': desiredHumor.url});
		result.update({'title': desiredHumor.title});
		result.update({'avgRating': desiredHumor.avgRating});
		result.update({'numRatings': desiredHumor.numRatings});		
		result.update({'createdBy': desiredHumor.createdBy.username});		
		result.update({'msg': desiredHumor.message});		
		result.update({'contentType': desiredHumor.contentType});
		
		if(request.user.is_authenticated()):
			curUser = request.user;
			myRating = Rating.objects.filter(user=curUser).filter(humor=desiredHumor);
			if(len(myRating) > 0):
				result.update({'rating': myRating[0].rating});
				result.update({'flag': myRating[0].flag});			

		return HttpResponse(simplejson.dumps(result), content_type='application/json');
	return HttpResponse("BAD");

def register(request):
	t = loader.get_template("archive.html")
	user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password']);
	user.save();
	humorContents = HumorContent.objects.order_by('id'); #do I have to login?
	mostRecent = humorContents[len(humorContents) - 1];
	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	c = RequestContext(request, { 'humorContent': mostRecent });
	if user is not None:
		if user.is_active:
			auth_login(request, user)
	return HttpResponse(t.render(c))
	

def addContent(request):
	t = loader.get_template("archive.html")
	newContent = HumorContent(contentType=request.POST['content_type'],title=request.POST['title'], createdBy=request.user);
	if (newContent.contentType=="Text"):
		newContent.message=request.POST['url'];
	else:
		newContent.url=request.POST['url'];
	newContent.save();
	c = RequestContext(request, { 'humorContent': newContent });
	return HttpResponse(t.render(c))

def getPrevHumor(request):
	if(request.GET.get('id')):
		humorContents = HumorContent.objects.order_by('id');
		index = 0;

		for i, j in enumerate(humorContents):
			if j.id == int(request.GET.get('id')):
				index = i;

		nextIndex = index - 1;
		nextIndex = ((nextIndex) % len(humorContents));
		desiredHumor = humorContents[nextIndex];
		result = {}
		result.update({'id': desiredHumor.id})
		result.update({'url': desiredHumor.url})
		result.update({'title': desiredHumor.title});
		result.update({'avgRating': desiredHumor.avgRating});
		result.update({'numRatings': desiredHumor.numRatings});
		result.update({'createdBy': desiredHumor.createdBy.username});		
		result.update({'msg': desiredHumor.message});		
		result.update({'contentType': desiredHumor.contentType});
		
		if(request.user.is_authenticated()):
			curUser = request.user;
			myRating = Rating.objects.filter(user=curUser).filter(humor=desiredHumor);
			if(len(myRating) > 0):
				result.update({'rating': myRating[0].rating});
				result.update({'flag': myRating[0].flag});

		return HttpResponse(simplejson.dumps(result), content_type='application/json');
	return HttpResponse("BAD");

## Registration Related ##
def regularuserRegistration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
			user.save()
			regularuser = RegularUser(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
			regularuser.save()
			return HttpResponseRedirect('/profile')
		else:
			return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
	else:
		''' user is not submitting the form, show them a blank registration form '''
		form = RegistrationForm()
		context = {'form': form}
		return render_to_response('register.html', context, context_instance=RequestContext(request))
