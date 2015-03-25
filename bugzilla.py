#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Copyright (c) 2015 Mozilla Corporation
# Author: Guillaume Destuynder <gdestuynder@mozilla.com>

# This is an ultra-simple implementation of the Bugzilla API as per
# http://bugzilla.readthedocs.org/en/latest/api/core/v1/

import json
import requests
try:
    import urllib.parse
    quote_url = urllib.parse.quote
except ImportError:
    #Well hello there python2 user!
    import urllib
    quote_url = urllib.quote
import base64

class DotDict(dict):
    '''dict.item notation for dict()'s'''
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Bugzilla:
    def __init__(self, url, api_key):
        self.api_key    = api_key
        if (url[-1] != '/'): url = url+'/'
        self.url        = url

    def quick_search(self, terms):
        '''Wrapper for search_bugs, for simple string searches'''
        assert type(terms) is str
        p = [{'quicksearch': terms}]
        return self.search_bugs(p)

    def search_bugs(self, terms):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/bug.html#search-bugs
        terms = [{'product': 'Infrastructure & Operations'}, {'status': 'NEW'}]'''
        params = ''
        for i in terms:
            k = i.popitem()
            params = '{p}&{new}={value}'.format(p=params, new=quote_url(k[0]),
                        value=quote_url(k[1]))
        return DotDict(self._get('bug', params=params))

    def get_bug(self, bugid):
        return DotDict(self._get('bug/{bugid}'.format(bugid=bugid))['bugs'][0])

    def get_comments(self, bugid):
        return self._get('bug/{bugid}/comment'.format(bugid=bugid))

    def get_comment(self, commentid):
        return self._get('bug/comment/{commentid}'.format(commentid=commentid))

    def get_attachments(self, bugid):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/attachment.html#get-attachment'''
        return DotDict(self._get('bug/{bugid}/attachment'.format(bugid=bugid))['bugs'])

    def get_attachment(self, attachmentid):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/attachment.html#get-attachment'''
        return self._get('bug/attachment/{attachmentid}'.format(attachmentid=attachmentid))

    def put_attachment(self, attachmentid, attachment_update):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/attachment.html#update-attachment'''
        assert type(attachment_update) is DotDict
        if (not 'ids' in attachment_update):
            attachment_update.ids = [attachmentid]

        return self._put('bug/attachment/{attachmentid}'.format(attachmentid=attachmentid),
                json.dumps(attachment_update))

    def put_bug(self, bugid, bug_update):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/bug.html#update-bug'''
        assert type(bug_update) is DotDict
        if (not 'ids' in bug_update):
            bug_update.ids = [bugid]

        return self._put('bug/{bugid}'.format(bugid=bugid),
                json.dumps(bug_update))

    def post_attachment(self, bugid, attachment):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/attachment.html#create-attachment'''
        assert type(attachment) is DotDict
        assert 'data' in attachment
        assert 'file_name' in attachment
        assert 'summary' in attachment
        if (not 'content_type' in attachment): attachment.content_type = 'text/plain'
        attachment.ids = bugid
        attachment.data = base64.standard_b64encode(bytearray(attachment.data, 'ascii')).decode('ascii')

        return self._post('bug/{bugid}/attachment'.format(bugid=bugid), json.dumps(attachment))

    def post_bug(self, bug):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/bug.html#create-bug'''
        assert type(bug) is DotDict
        assert 'product' in bug
        assert 'component' in bug
        assert 'summary' in bug
        if (not 'version' in bug): bug.version = 'other'
        if (not 'op_sys' in bug): bug.op_sys = 'All'
        if (not 'platform' in bug): bug.platform = 'All'

        return self._post('bug', json.dumps(bug))

    def post_comment(self, bugid, comment):
        '''http://bugzilla.readthedocs.org/en/latest/api/core/v1/comment.html#create-comments'''
        data = {'id': bugid, "comment": comment}
        return self._post('bug/{bugid}/comment'.format(bugid=bugid), json.dumps(data))

    def _get(self, q, params=''):
        '''Generic GET wrapper including the api_key'''
        if (q[-1] == '/'): q = q[:-1]
        headers = {'Content-Type': 'application/json'}
        r = requests.get('{url}{q}?api_key={key}{params}'.format(url=self.url, q=q, key=self.api_key, params=params),
                        headers=headers)
        ret = DotDict(r.json())
        if (not r.ok or ('error' in ret and ret.error == True)):
            raise Exception(r.url, r.reason, r.status_code, r.json())
        return DotDict(r.json())

    def _post(self, q, payload='', params=''):
        '''Generic POST wrapper including the api_key'''
        if (q[-1] == '/'): q = q[:-1]
        headers = {'Content-Type': 'application/json'}
        r = requests.post('{url}{q}?api_key={key}{params}'.format(url=self.url, q=q, key=self.api_key, params=params),
                        headers=headers, data=payload)
        ret = DotDict(r.json())
        if (not r.ok or ('error' in ret and ret.error == True)):
            raise Exception(r.url, r.reason, r.status_code, r.json())
        return DotDict(r.json())

    def _put(self, q, payload='', params=''):
        '''Generic PUT wrapper including the api_key'''
        if (q[-1] == '/'): q = q[:-1]
        headers = {'Content-Type': 'application/json'}
        r = requests.put('{url}{q}?api_key={key}{params}'.format(url=self.url, q=q, key=self.api_key, params=params),
                        headers=headers, data=payload)
        ret = DotDict(r.json())
        if (not r.ok or ('error' in ret and ret.error == True)):
            raise Exception(r.url, r.reason, r.status_code, r.json())
        return ret
