from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.context_processors import csrf
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from WebPortal.models import HumorContent, Rating
from django.db.models import Max
import numpy as np
import sys
from sklearn.decomposition import ProjectedGradientNMF

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
		print "hey1"
		if(len(myRating) > 0): #rating exists
			myRating = myRating[0];
			myRating.flag = not myRating.flag;

			if(myRating.flag):
				humorContent.numFlags += 1;
			else:
				humorContent.numFlags -= 1;
			
			myRating.save();
		else: #new rating
			myRating = Rating();
			myRating.user = curUser;
			myRating.humor = humorContent;
			myRating.flag = True;
			myRating.rating = 0;
			humorContent.numFlags = humorContent.numFlags + 1;
			myRating.save();

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
			if(oldRating is not None and int(oldRating) != 0):
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

def getRecommendation(request):

	if(request.GET.get('id')):
		
		humorContents = HumorContent.objects.order_by('id');

		max_user_index = Rating.objects.aggregate(Max('user'))['user__max']
		max_humor_index = Rating.objects.aggregate(Max('humor'))['humor__max']

		ratings = Rating.objects.order_by('humor');

		ratings_matrix_raw = [[0 for n in range(max_humor_index)] for m in range(max_user_index)]
		ratings_matrix = [[3 for n in range(max_humor_index)] for m in range(max_user_index)]

		for i, j in enumerate(ratings):
			ratings_matrix[j.user_id-1][j.humor_id-1] = j.rating
			ratings_matrix_raw[j.user_id-1][j.humor_id-1] = j.rating

		ratings_matrix = np.reshape(ratings_matrix, (max_user_index, max_humor_index))

		recommendedIndex = recommend(ratings_matrix, ratings_matrix_raw, request.user.id-1) + 1 

		index = 0;

		for i, j in enumerate(humorContents):
			if j.id == recommendedIndex:
				index = i;

		desiredHumor = humorContents[index];
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


def recommend(matrix_3filled, matrix_raw, user, numOfNeighbors=5):
    
    	model = ProjectedGradientNMF(n_components=2, init='random', random_state=0)
    	model.fit(matrix_3filled)
    	transformed = np.dot(model.fit_transform(matrix_3filled), model.components_)
    
   	neighbors=[]
    	distances = np.sum((transformed-transformed[user])**2, axis=1)

    	for x in xrange(numOfNeighbors):
        	distances[np.argmin(distances)] = sys.float_info.max
        	neighbors.append(np.argmin(distances))

    	average=[0.0]*transformed.shape[1]
    	for x in xrange(numOfNeighbors):
        	average += transformed[neighbors[x]]
    	average = average/numOfNeighbors
    	unratedItems=[]
    	for x in xrange(np.shape(matrix_raw)[1]):
        	if matrix_raw[user][x] == 0:
            		unratedItems.append(x)
    

    	if len(unratedItems) is 0:
        	item = np.argmax(average)
        	return item
    	else:
        	maxAverage = 0
        	item = np.argmax(average)
        	for x in xrange(len(unratedItems)):
            		if average[unratedItems[x]] > maxAverage:
                		maxAverage = average[unratedItems[x]] 
                		item = unratedItems[x]
        	return item
