#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''This program dumps the whole case (scandal) in a text form, as UTF-8 text.'''

import codecs
import locale
import sys
import getopt

from getopt import gnu_getopt as getopts

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
#sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 

import orm

OUTFILE=None
DB='produkcja'

#sys.setdefaultencoding('utf-8')

def output(data):

  if not isinstance(data, unicode):
    data = data.decode('utf-8')
    
  if OUTFILE:
    OUTFILE.write(data)
    OUTFILE.write('\r\n')
  else:
    print data



def help():
  print '''%s [ -o <filename> ] [ --all | --list | <case id > ] 

  --list    -l  list cases 
  --all     -a  dump all cases
  --output  -o  output file
''' % sys.argv[0]

  sys.exit(0)
  
if __name__ == '__main__':

  try: 
    if len(sys.argv) > 1:
      args, params = getopts(sys.argv[1:], 'hlao:', ('help', 'all', 'list', 'output='))

      for opt, param in args:
        o = opt.strip('-')
        if o in ('a', 'all'):
          pass # all cases are already in cases
        elif o in ('l', 'list'):
          for c in orm.query('cases',db=DB):
            print '%s: %s' % ( c[0], c[1][0] ) 
          sys.exit(0)
        elif o in ('o', 'output'): 
          OUTFILE = codecs.open(param, mode='w', encoding='utf-8')          
        elif o in ('h', 'help'):
          help()
          
      if params:
        cases = orm.query('case_id', str(int(params[0])), db=DB)
      else:
        cases = orm.query('cases',db=DB)
        
  except getopt.GetoptError:
    help()
  
  for case in cases:

    output( "SPRAWA: %s" % ' / '.join(case[1])) 

    output( "OPIS: %s" % case[2])

    output( "TYP[Y] KORUPCJI: %s" % ' / '.join([item[1] for item in orm.query('scandal_types', case[0], DB)]))

    output( "SFERY KORUPCJI: %s" % ' / '.join([item[1] for item in orm.query('scandal_fields', case[0], DB)]))

    events = orm.query ('case_events', case[0], DB)

    for event in events:

      output( '\nWYDARZENIE: %s' % unicode(event[6]))

      output( 'LOKALIZACJA: %s' % event[7])

      output( 'DATA: %s' % event [1])
      output( 'TYP[Y]: %s' % ' / '.join([item[1] for item in orm.query('event_types', event[0], DB)]))
      output( 'OPIS: %s' % event[2] )

      actors = orm.query('event_actors', event[0], DB)

      for actor in actors:
        output( '\nAKTOR: %s' % actor[1])
        output( 'OSOBA: %s' % ('tak' if actor[4] else 'nie'))

        output( 'TYP[Y] AKTORA: %s' % ' / '.join ( [item[1] for item in orm.query('actor_event_types' , (actor[0], event[0]), DB)] ))

        output( 'ROLA AKTORA: %s' % ' / '.join ( [item[1] for item in orm.query('actor_event_roles' , (actor[0], event[0]), DB)] ))
    
        output( 'AFILIACJE AKTORA: %s' % ' / '.join ( [item[1] for item in orm.query('actor_event_affiliations' , (actor[0], event[0]), DB)] ))
        
      refs = orm.query('event_refs', event[0], DB)
      if refs:
        output( 'ŻRÓDŁA:')

        for ref in refs:
          try:
            output( u' * %s, %s %s, Dostęp: %s,\n   URL: %s' % ref[1:])
          except TypeError:
            pass
      
  
