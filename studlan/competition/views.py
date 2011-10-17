# -*- encoding: utf-8 -*-

from studlan.competition.models import Activity, Competition
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

def main(request):
	competitions = Competition.objects.all()

	for c in competitions:
		if len(c.desc) >= 200:
			c.desc = c.desc[:197] + '...'
			
	return render_to_response('competitions.html', {'competitions': competitions},
							  context_instance=RequestContext(request))

def single(request, competition_id):
	competition = get_object_or_404(Competition, pk=competition_id)
	return render_to_response('competition.html', {'competition': competition},
							  context_instance=RequestContext(request))