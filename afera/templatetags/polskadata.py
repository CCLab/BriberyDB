# -*- coding: utf-8

from django import template

import datetime

months = (None, u'stycznia', u'lutego', u'marca', u'kwietnia', u'maja', u'czerwca', u'lipca', u'sierpnia', u'września', u'października', u'listopada', u'grudnia')

register = template.Library()

@register.filter(name='polskadata')
def polskadata(val, arg=None):

  if isinstance(val, datetime.date):
  
    result = "%d %s %d" % ( val.day, months[val.month], val.year )
  
  return result
  