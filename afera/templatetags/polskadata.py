from django import template

import datetime

months = ('stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'wrzesnia', 'pazdziernika', 'listopada', 'grudnia')

register = template.Library()

@register.filter(name='polskadata')
def polskadata(val, arg=None):

  if isinstance(val, datetime.date):
  
    result = "%d %s %d" % ( val.day, months[val.month], val.year )
  
  return result
  