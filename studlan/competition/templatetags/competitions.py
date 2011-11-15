from django import template
from studlan.competition.models import Competition

register = template.Library()

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
		#try:
		for c in Competition.objects.all():
			if context['request'].user in c.participants.all():
				user_in += '''
				<dt><a href="%s">%s</a></dt>
				<dd><span class="label %s">%s</span></dd>
				''' % ('/competitions/'+str(c.id)+'/', c.title, c.status_label(), c.status_text())
		#except:
		#		pass
		return user_in

register.tag('num_of_competitions', do_num_of_competitions)
register.tag('user_in', get_competitions_user_is_participating_in)