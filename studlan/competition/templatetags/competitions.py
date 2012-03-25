
import logging

from django import template
from django.core.urlresolvers import reverse

from studlan.competition.models import Competition

register = template.Library()

#--- For competition ---



#--- For sidebar ---

def do_num_of_competitions(parser, token):
	#tag_name, format_string = token.split_contents()
	
	return Competition_Renderer(len(Competition.objects.all()))

def get_competitions_user_is_participating_in(parser, token):
	return Competition_Participation_Renderer()

class Competition_Renderer(template.Node):
	def __init__(self, num_of_competitions):
		self.num_of_competitions = num_of_competitions
	def render(self, context):
		return self.num_of_competitions

class Competition_Participation_Renderer(template.Node):
	#def __init__(self):

	def render(self, context):
		user_in = ''
		# TODO Fix this derp
		try:
			for c in Competition.objects.all():
				if c.use_teams:
					for t in c.teams.all():
						if context['request'].user == t.leader or context['request'].user in t.members:
							user_in += '''
								<dt><a href="%s">%s</a></dt>
								<dd>
								''' % (reverse("competition", args=[c.id]), unicode(c))
							user_in += 'As [%s]%s<br/>' % (t.tag, t.title)
							user_in += '''
								<span class="label %s">%s</span></dd>
								''' % (c.status_label(), c.status_text_verbose())
				else:
					if context['request'].user in c.participants.all():
						user_in += '''
					    	<dt><a href="%s">%s</a></dt>
							<dd>As self<br/><span class="label %s">%s</span></dd>
							''' % (reverse("competition", args=[c.id]), unicode(c), c.status_label(), c.status_text_verbose())
		except:
			#TODO: fix team participations in sidebar.
			print "TODO: fix team participations in sidebar."
			pass
		finally:
			if user_in != '':
				return '<h5>Participating in</h5>' + user_in
			else:
				return user_in

register.tag('num_of_competitions', do_num_of_competitions)
register.tag('user_in', get_competitions_user_is_participating_in)
