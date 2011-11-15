from django import template
from studlan.competition.models import Competition

register = template.Library()

def do_alerts(parser, token):
	#tag_name, format_string = token.split_contents()
	return Alerts_Renderer()

class Alerts_Renderer(template.Node):
	#def __init__(self, alert):
	def render(self, context):
		request = context['request']
		try:
			alert = '''
			<div class="alert-message fade in %s" data-alert>
                <a class="close" href="#">x</a>
                <p>%s</p>
            </div>
			''' % (request.session['alert_label'], request.session['alert_message'])
		except:
			alert = ''
		return alert


register.tag('get_alerts', do_alerts)