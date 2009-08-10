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
Comments Macro

This macro display the comments page.
It collects the comments files and displays its content.

Usage:
    <<Comments(@PAGE@)>> on the Comments page
"""

# General imports:
import os
import glob
import pickle
from string import letters, digits
from random import choice

# MoinMoin imports
from MoinMoin.Page import Page

def read_comment( file_name ):
    f = open(file_name, 'r')
    comment = pickle.load(f)
    f.close()
    return comment

# Auxiliary function:
def Comments(request, pagename):
    def cmp_time( a, b ):
        if a['time'] < b['time']:
            return -1
        elif a['time'] > b['time']:
            return 1
        else:
            return 0

    def comment_html(comment, gettext ):
        _ = gettext
        return '''<table>
    <tr><td>%(name)s</td><td>%(comment_name)s</td></tr>
    <tr><td>%(time)s</td><td>%(comment_time)s</td></tr>
    <tr><td colspan=2>%(comment_text)s</td></tr>
    </table>''' % {
        'name': _('Name:'),
        'comment_name': comment['user_name'],
        'time': _('Time:'),
        'comment_time': comment['time'],
        'comment_text': '<p>'.join( comment['comment'].split('\n') ),
        }

    """
    Returns comments in page context.
    """
    _ = request.getText

    # Get the configuration:
    DISPLAY_NUMBER = request.cfg.comment_display_number
    OVERLAP_NUMBER = request.cfg.comment_overlap_number

    page = Page(request, pagename )
    comments_dir = page.getPagePath("comments", check_create=1)

    formatter = request.html_formatter
    html = ''

    files = glob.glob(os.path.join(comments_dir,'*.txt'))

    if not files:
        html = u'<p>%s</p>' % _('There are no comments')

    else:
        # Get the file names
        comments = [ read_comment(Xi) for Xi in files]

        # Order by name (remember that the first chars of the name represent the time)
        comments.sort(cmp_time)

        # Manage the Pagination
        # The last DISPLAY_NUMBER comments are visible while the remaining
        # are hidden and only displayed on demand (link inside the page)
        # It allows the display without the hide feature if remaining comments
        # do not exceed the OVERLAP_NUMBER.
        if len(comments)>DISPLAY_NUMBER+OVERLAP_NUMBER:
            visible_comments = comments[:DISPLAY_NUMBER]
            hidden_comments = comments[DISPLAY_NUMBER:]
        else:
            visible_comments = comments
            hidden_comments = []

        for comment in visible_comments:
            html += u"%s" % comment_html( comment, _ )

        if hidden_comments:
            # To avoid display problems if macro is used several times in the same page.
            div_id = ''.join([choice(letters + digits) for i in range(3)])

            html += u"""<a href="#" onClick = showAndHide('%(div_id)s')>
            %(msg)s</a>
            <div id='%(div_id)s' style="display:none"><br />""" % {
                'div_id': div_id,
                'msg': _('Show/Hide the next %s comments'%len(hidden_comments))}

            for comment in hidden_comments:
                html += u"%s" % comment_html( comment, _ )

            html += u"</div>"

            # Place the javascript to hide and show the comments
            # NOTE: If used more than one time in the same page this part is repeated,
            # it should work but it's not the best HTML code.
            html += u"""
<script language="JavaScript">
function showAndHide(theId)
{
   var el = document.getElementById(theId)

   if (el.style.display=="none")
   {
      el.style.display="block"; //show element
   }
   else
   {
      el.style.display="none"; //hide element
   }
}
</script>
        """

    return formatter.rawHTML(html)

# Macro function:
def macro_Comments(macro, pagename=u''):
    return Comments(macro.request, pagename)
