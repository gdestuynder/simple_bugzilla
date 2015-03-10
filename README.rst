Simple Bugzilla interface
=========================

Why?
====
Because other libraries I found had limited API support (like no attachment support), complex implementation, and don't seem very supported/taking
PRs :)

For example most of what can be done with a 1000SLOC lib is done in this one with 100SLOC.

Usage
=====

You can and should get an API KEY from Bugzilla with a Bugzilla account to your instance, in the user preferences.
Everything is basically a DocDict (a dict() you can address like an object i.e. dict['x'] is also dict.x).
The contents of the DotDict reflects the exact output of the API, i.e. any JSON the API sends is what you'll find in the
DotDict. Any data you need to send to the API uses the same names as well.
See full doc at http://bugzilla.readthedocs.org/en/latest/api/core/v1/ or/and just look at the output of the examples.

Examples
--------

.. code:: Python

        import bugzilla
        
        b = bugzilla.Bugzilla(url="https://bugzilla-dev.allizom.org/rest/", api_key="your api key")
        #Just getting a bug
        bug = b.get_bug(1001)
        print(bug.id, bug.status)
        #All attributes - it's just a dot dict.
        print(bug)
        
        #Making a bug
        bug = bugzilla.DotDict()
        bug.product = 'My product'
        bug.component = 'My component'
        bug.summary = 'A test bug'
        bug.whiteboard 'my_flag'
        print(b.post_bug(bug))

        #Adding an attachment
        attachment = bugzilla.DotDict()
        attachment.file_name = 'clowns.txt'
        attachment.summary = 'Test attachement'
        attachment.data = 'some ASCII content'
        print(b.post_attachment(1001, attachment))

        #Search for stuff
        terms = [{'product': 'MyProduct'}, {'product': 'MyOtherProduct'}, {'status': 'NEW'}]
        print(b.search_bugs(terms))
        #Or more easily
        print(b.quick_search('test bug'))


TODO
====

- Currently it does not work without an API key.
- Currently only support ASCII attachments as string.
- Some more obscure API methods are not implemented, like classifieds.
