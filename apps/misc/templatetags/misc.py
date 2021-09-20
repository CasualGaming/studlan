# -*- coding: utf-8 -*-

from django.template import Library


register = Library()


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the sviews
    """
    return range(value)


@register.filter
def get_range1(value):
    return range(1, value + 1)


@register.filter
def get_user_ticket(tickets, user):
    return tickets[user].ticket_type


@register.filter
def get_dict_val(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def divide(dividend, divisor):
    if divisor == 0:
        return 0
    return dividend / float(divisor)


@register.simple_tag
def divide_percent(dividend, divisor):
    if divisor == 0:
        return '0%'
    return '{val:.2f}%'.format(val=(dividend / float(divisor) * 100))


@register.simple_tag
def subtract(minuend, subtrahend):
    return minuend - subtrahend
