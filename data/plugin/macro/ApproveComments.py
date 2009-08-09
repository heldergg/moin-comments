# -*- coding: utf-8 -*-

# Moin-comments - Blog like comments in MoinMoin
# Copyright (C) 2009 José Lopes

## This file is part of Moin-comments.
##
## Moin-comments is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Moin-comments is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Moin-comments.  If not, see <http://www.gnu.org/licenses/>.

#
# José Lopes <jose.lopes@paxjulia.com>
#
# $Id$
#

"""
Approve Comments Macro

This macro lists the comments waiting for approval and displays the
delete and approval buttons.

Usage:
    <<ApproveComments()>>

Requirements:
    You must define the correct path at WORK_DIR
"""

# General imports:
import os
from string import split, replace
import glob

# Auxiliary function:
def ApproveComments(request):
    """
    Render comments form in page context.
    """
    _ = request.getText

    # Configuration:
    PAGES_DIR = os.path.join(request.cfg.data_dir, 'pages')
    APPROVAL_PAGE = request.cfg.comment_approval_page
    APPROVAL_DIR = os.path.join(PAGES_DIR, APPROVAL_PAGE)

    formatter = request.html_formatter
    html = ''

    files = glob.glob('%s/*.txt' % APPROVAL_DIR)

    if not files:
        html = u'<p>%s</p>' % _("There's no comment awaiting for moderation.")
    else:
        # Organize files by page
        info = {}
        for file in files:
            file = split(file, '/')
            title = split(file[-1], '-')
            if not info.has_key(title[0]):
                info[title[0]] = []
            info[title[0]].append(title[1])

        for key in info:
            comments = info[key]
            comments.sort()
            comments.reverse()

            for comment in comments:

                data = open(os.path.join(APPROVAL_DIR, '%s-%s' % (key, comment)), 'r')
                lines = data.read().decode('utf-8')
                data.close()

                if lines:
                    html += u"""
<div class="comment_approval">
<table>
    <tr>
        <th>%(intro)s %(page_name)s</th>
    </tr>
    <tr>
        <td>%(comment_text)s</td>
    </tr>
    <tr>
        <td>
            <form method="POST" action="/%(approval_page)s">
            <input type="hidden" name="action" value="comment_delete">
            <input type="submit" value="%(button_delete)s" id="delete">
            <input type="hidden" name="file" value="%(key_comment)s">
            </form>
            <form method="POST" action="/%(approval_page)s">
            <input type="hidden" name="action" value="comment_approve">
            <input type="submit" value="%(button_accept)s" id="ok">
            <input type="hidden" name="file" value="%(key_comment)s">
            </form>
        </td>
    </tr>
</table>
</div><br />
            """ % {
                'approval_page': APPROVAL_PAGE,
                'page_name': replace(key,'_','/'),
                'comment_text': lines,
                'key_comment': u'%s-%s' % (key, comment),
                'button_delete': _('Delete'),
                'button_accept': _('Accept'),
                'intro': _('Comment to') }

                else: # If the file is empty:
                    html += u"""
<div class="comment_approval">
<table>
    <tr>
        <th colspan=2>%(intro)s %(page_name)s</th>
    </tr>
    <tr>
        <td>%(error)s</td>
        <td>
            <form method="POST" action="/%(approval_page)s">
            <input type="hidden" name="action" value="comment_delete">
            <input type="submit" value="%(button_delete)s">
            <input type="hidden" name="file" value="%(key_comment)s">
            </form>
        </td>
    </tr>
</table>
</div><br />
            """ % {
                'approval_page': APPROVAL_PAGE,
                'error': _('Empty comment, it should be deleted.'),
                'page_name': replace(key,'_','/'),
                'key_comment': u'%s-%s' % (key, comment),
                'intro': _('Comment to'),
                'button_delete': _('Delete') }

    return formatter.rawHTML(html)

# Macro function:
def macro_ApproveComments(macro):
    return ApproveComments(macro.request)
