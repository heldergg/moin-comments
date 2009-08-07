# -*- coding: utf-8 -*-

# Moin-comments - Blog like comments in MoinMoin
# Copyright (C) 2009 José Lopes

## This file is part of WebPyMail.
##
## WebPyMail is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## WebPyMail is distributed in the hope that it will be useful,
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
By José Lopes - Bombolom.com

This macro display the comments page.
It collects the comments files and displays its content.

Usage:
    <<Comments(@PAGE@)>> on the Comments page
"""

# General imports:
import os
from string import replace, split, letters, digits
import glob
from random import choice

# Get the configuration values
conf = {}
current_dir =  os.path.dirname(__file__)
conf_file = os.path.join(current_dir, 'comments_config.txt')

data = open(conf_file, 'r')
lines = data.readlines()
data.close()
for line in lines:
    line = replace(line, '\n', '')
    line = split(line, '==')
    conf[line[0]]=line[1]

PAGES_DIR = os.path.join(os.path.split(os.path.split(current_dir)[0])[0], 'pages')
DISPLAY_NUMBER = int(conf['DISPLAY_NUMBER'])
OVERLAP_NUMBER = int(conf['OVERLAP_NUMBER'])

# Auxiliary function:
def Comments(request, pagename):
    """
    Returns comments in page context.
    """
    formatter = request.html_formatter
    html = ''

    pagename = replace(pagename, '/', '(2f)')

    # Check if comments directory exists and creates it if not
    comments_dir = os.path.join(PAGES_DIR, pagename, 'comments')

    if not os.path.exists(comments_dir):
            os.mkdir(comments_dir)

    files = glob.glob('%s/*.txt' % comments_dir)

    if not files:
        html = u"""
<p>Não existe nenhum comentário</p>
        """

    else:
        # Get the file names
        comments = [split(Xi, '/')[-1] for Xi in files]

        # Order by name (remember that the first chars of the name represent the time)
        comments.sort()
        comments.reverse()

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
            data = open(os.path.join(comments_dir, comment), 'r')
            lines = data.read().decode('utf-8')
            data.close()
            html += u"%s" % lines

        if hidden_comments:
            # To avoid display problems if macro is used several times in the same page.
            div_id = ''.join([choice(letters + digits) for i in range(3)])

            html += u"""
<a href="#" onClick = showAndHide('%s')>Mostar / Esconder os restantes %s comentários</a>
<div id='%s' style="display:none"><br />""" % (div_id, len(hidden_comments), div_id)

            for comment in hidden_comments:
                data = open(os.path.join(comments_dir, comment), 'r')
                lines = data.read().decode('utf-8')
                data.close()
                html += u"%s" % lines

            html += u"</div>"

            # Place the javascript to hide and show the comments
            # NOTE: If used more than one time in the same page this part is repeated,
            # no problem about it but its not the best HTML code.
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
