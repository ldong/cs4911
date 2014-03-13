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
	return HttpResponse(t.render(c))

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
			newAverage = ((oldAverage * weight) + newRating - oldRating) / (humorContent.numRatings);
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
		idNumber = int(request.GET.get('id'));
		nextId = ((idNumber) % len(humorContents));
		desiredHumor = humorContents[nextId];
		result = {}
		result.update({'id': desiredHumor.id});
		result.update({'url': desiredHumor.url});
		result.update({'title': desiredHumor.title});
		result.update({'avgRating': desiredHumor.avgRating});
		result.update({'numRatings': desiredHumor.numRatings});
		
		if(request.user.is_authenticated()):
			curUser = request.user;
			myRating = Rating.objects.filter(user=curUser).filter(humor=desiredHumor);
			if(len(myRating) > 0):
				result.update({'rating': myRating[0].rating});			

		return HttpResponse(simplejson.dumps(result), content_type='application/json');
	return HttpResponse("BAD");

def getPrevHumor(request):
	if(request.GET.get('id')):
		humorContents = HumorContent.objects.order_by('id');
		idNumber = int(request.GET.get('id')) - 2;
		prevId = ((idNumber) % len(humorContents));
		desiredHumor = humorContents[prevId];
		result = {}
		result.update({'id': desiredHumor.id})
		result.update({'url': desiredHumor.url})
		result.update({'title': desiredHumor.title});
		result.update({'avgRating': desiredHumor.avgRating});
		result.update({'numRatings': desiredHumor.numRatings});
		
		if(request.user.is_authenticated()):
			curUser = request.user;
			myRating = Rating.objects.filter(user=curUser).filter(humor=desiredHumor);
			if(len(myRating) > 0):
				result.update({'rating': myRating[0].rating});

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
