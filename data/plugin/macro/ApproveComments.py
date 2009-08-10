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
import pickle
from datetime import datetime
import glob

def read_comment( file_name ):
    f = open(file_name, 'r')
    comment = pickle.load(f)
    f.close()
    return comment

# Auxiliary function:
def ApproveComments(request):
    """
    Render comments form in page context.
    """
    def cmp_page_time( a, b ):
        if a['page'] < b['page']:
            return -1
        elif a['page'] > b['page']:
            return 1
        else:
            if a['time'] < b['time']:
                return -1
            elif a['time'] > b['time']:
                return 1
        return 0

    _ = request.getText

    # Configuration:
    PAGES_DIR = os.path.join(request.cfg.data_dir, 'pages')
    APPROVAL_PAGE = request.cfg.comment_approval_page
    APPROVAL_DIR = os.path.join(PAGES_DIR, APPROVAL_PAGE)

    formatter = request.html_formatter
    html = ''

    files = glob.glob(os.path.join(APPROVAL_DIR,'*.txt'))

    if not files:
        html = [u'<p>%s</p>' % _("There's no comment awaiting for moderation.")]
    else:
        comments = []

        # Read the comments:
        for file_name in files:
            comment = read_comment( file_name )
            comments.append(comment)
            comments[-1]['file_name'] = file_name

        # Sort the coments by page, then by time
        comments.sort(cmp_page_time)

        html = []
        for comment in comments:
            html.append( u"""<div class="comment_approval">
<table>
    <tr>
        <th colspan=2>%(intro)s %(page_name)s</th>
    </tr>
    <tr><td>%(name)s</td><td>%(comment_name)s</td></tr>
    <tr><td>%(time)s</td><td>%(comment_time)s</td></tr>
    <tr><td colspan=2>%(comment_text)s</td></tr>
    <tr>
        <td colspan=2>
            <form method="POST" action="/%(approval_page)s">
            <input type="hidden" name="action" value="comment_delete">
            <input type="submit" value="%(button_delete)s" id="delete">
            <input type="hidden" name="file" value="%(comment_file)s">
            </form>
            <form method="POST" action="/%(approval_page)s">
            <input type="hidden" name="action" value="comment_approve">
            <input type="submit" value="%(button_accept)s" id="ok">
            <input type="hidden" name="file" value="%(comment_file)s">
            <input type="hidden" name="page_name" value="%(page_name)s">
            </form>
        </td>
    </tr>
</table>
</div><br />""" % {
                'intro': _('Comment to'),
                'page_name': comment['page'],
                'name': _('Name:'),
                'time': _('Time:'),
                'comment_time': comment['time'],
                'comment_name': comment['user_name'],
                'comment_text': '<p>'.join( comment['comment'].split('\n') ),
                'comment_file': comment['file_name'],
                'approval_page': APPROVAL_PAGE,
                'button_delete': _('Delete'),
                'button_accept': _('Accept'),
                 } )

    return formatter.rawHTML('\n'.join(html))

# Macro function:
def macro_ApproveComments(macro):
    return ApproveComments(macro.request)
