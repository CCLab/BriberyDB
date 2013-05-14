BriberyDB
=========

Database and webapplication for storing and display of bribery cases in Poland.


Remarks
-------

This is a Django app with a little unconventional architecture that is a
result of integration of legacy database with the project.

There are two databases defined in settings: 'default' (used by Django) and
'afery', a legacy database that stores the information about bribery and
corruption cases. This database is maintained using the cuckoo codebase
(<https://github.com/CCLab/cuckoo>).

The second database is queried using predefined set of raw SQL queries,
stored called from orm.py module.

The default database is not used in the moment, it is meant to store
CMS-related information - the static pages and the front page content.


Third party software
--------------------

The timeline display utilizes the TimelineJS software by VeriteCo, from
<https://github.com/VeriteCo/TimelineJS>. 
