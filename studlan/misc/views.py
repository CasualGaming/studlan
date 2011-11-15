# -*- encoding: utf-8 -*-
from django.http import HttpResponse

# This is accessed asynchronicly to remove alerts via jquery
def remove_alerts(request):
	try:
		del request.session['alert_label']
		del request.session['alert_message']
	except:
		pass
	return HttpResponse('OK')