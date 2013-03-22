#! /usr/bin/env python
# -*- coding: utf-8 -*-

import orm

DB='produkcja'

if __name__ == '__main__':

  cases = orm.query('cases',db=DB)

  for case in cases[:1]:

    print "SPRAWA: %s" % ' / '.join(case[1])

    print "OPIS:, %s" % case[2]

    print "TYP[Y] KORUPCJI: %s" % ' / '.join([item[1] for item in orm.query('scandal_types', case[0], DB)])

    print "SFERY KORUPCJI: %s" % ' / '.join([item[1] for item in orm.query('scandal_fields', case[0], DB)])

    events = orm.query ('case_events', case[0], DB)

    for event in events:

      print '\nWYDARZENIE: %s' % unicode(event[6])

      print 'LOKALIZACJA: %s' % event[7]

      print 'DATA: %s' % event [1]
      print 'TYP[Y]: %s' % ' / '.join([item[1] for item in orm.query('event_types', event[0], DB)])
      print 'OPIS: %s' % event[2]

      actors = orm.query('event_actors', event[0], DB)

      for actor in actors:
        print '\nAKTOR: %s' % actor[1]
        print 'OSOBA: %s' % ('tak' if actor[4] == 't' else 'nie')

        print 'TYP[Y] AKTORA: %s' % ' / '.join ( [item[1] for item in orm.query('actor_event_types' , (actor[0], event[0]), DB)] )

        print 'ROLA AKTORA: %s' % ' / '.join ( [item[1] for item in orm.query('actor_event_roles' , (actor[0], event[0]), DB)] )
    
        print 'AFILIACJE AKTORA: %s' % ' / '.join ( [item[1] for item in orm.query('actor_event_affiliations' , (actor[0], event[0]), DB)] )
        
      refs = orm.query('event_refs', event[0], DB)
      if refs:
        print 'ŻRÓDŁA:'

        for ref in refs:
          print u' * %s, %s %s, Dostęp: %s, URL %s' % ref[1:]
      

    
