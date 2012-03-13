# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import Http404

# This is accessed asynchronously to remove alerts via jquery
def remove_alert(request):
	try:
		pass
	except:
		pass
	return HttpResponse('')

def arrivals(request):
	if not request.user.is_staff:
		raise Http404
	users = User.objects.all()
	sorted_users = []
	for u in users:
		sorted_users.append(u)
	sorted_users.sort(key=lambda x: x.username.lower(), reverse=False)
	return render_to_response('arrivals.html', {'users': sorted_users}, context_instance=RequestContext(request))

def toggle_arrival(request, user_id):
	if not request.user.is_staff:
		raise Http404
	user = get_object_or_404(User, pk=user_id)
	if user.get_profile().has_payed:
		user.get_profile().has_payed = False
	else:
		user.get_profile().has_payed = True
	user.get_profile().save()
	user.save()
	return redirect('arrivals')