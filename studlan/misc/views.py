# -*- encoding: utf-8 -*-
from django.http import HttpResponse

# This is accessed asynchronicly to remove alerts via jquery
def remove_alert(request):
	try:
		pass
	except:
		pass
	return HttpResponse('')