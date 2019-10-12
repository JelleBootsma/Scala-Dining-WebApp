from django import template
from django.conf import settings
from django.template.defaulttags import Node, url

register = template.Library()


class FullURLNode(Node):
    """It's a shell for URL_node.

    This is easier than copying the entire compilation function to intercept the Node creation.
    """

    def __init__(self, url_node):
        self.url_node = url_node
        self.domain_name = self.url_node.kwargs.pop('domain_name', settings.DOMAIN_NAME)

    def render(self, context):
        url_string = self.url_node.render(context)

        if self.url_node.asvar:
            context[self.url_node.asvar] = "https://" + self.domain_name + context[self.url_node.asvar]
            return ''
        else:
            url_string = "https://" + self.domain_name + url_string
            return url_string


@register.tag
def full_url(parser, token):
    return FullURLNode(url(parser, token))


@register.filter
def to_full_url(url_string, domain_name=settings.DOMAIN_NAME):
    return "https://" + domain_name + url_string.__str__()
