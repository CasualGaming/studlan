from django import template
from studlan.competition.models import Competition

register = template.Library()

def do_num_of_competitions(parser, token):
	#tag_name, format_string = token.split_contents()
	
	return Competition_Renderer(len(Competition.objects.all()))

class Competition_Renderer(template.Node):
	def __init__(self, num_of_competitions):
		self.num_of_competitions = num_of_competitions
	def render(self, context):
		return self.num_of_competitions


register.tag('num_of_competitions', do_num_of_competitions)