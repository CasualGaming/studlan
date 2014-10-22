from django import template
from studlan.news.models import Article

register = template.Library()

def do_num_of_articles(parser, token):
	#tag_name, format_string = token.split_contents()
	
	return News_Renderer(len(Article.objects.all()))

class News_Renderer(template.Node):
	def __init__(self, num_of_articles):
		self.num_of_articles = num_of_articles
	def render(self, context):
		return self.num_of_articles


register.tag('num_of_articles', do_num_of_articles)