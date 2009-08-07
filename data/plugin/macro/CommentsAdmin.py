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
Comments Administration Macro

This macro adds an administration functionality to the comments
feature.
It can be place anywhere, like for instance the wiki menu, and if the
user is a SuperUser he will see the link to the comments approval page,
with the total of comments waiting for approval.

 Usage:
    <<CommentsAdmin()>>
    or
    <<CommentsAdmin(Some header text)>>
"""
# General imports:
import os
import glob
from string import split, replace

# MoinMoin imports:
from MoinMoin import user

def CommentsAdmin(request, header_text):
    """
    Providing the link to the approval page in any place the user sees fit.
    """

    # Configuration:
    PAGES_DIR = os.path.join(request.cfg.data_dir, 'pages')
    APPROVAL_PAGE = request.cfg.comment_approval_page
    APPROVAL_DIR = os.path.join(PAGES_DIR, APPROVAL_PAGE)

    formatter = request.html_formatter
    html = ''

    if request.user.isSuperUser():
        if header_text:
            html += '<strong>%s</strong><br /><br />' % header_text

        # Calculate the number of comments waiting for approval
        files = glob.glob('%s/*.txt' % APPROVAL_DIR)
        total_waiting = len(files)

        html += u"""
    <a href="%s">Aprovar Comentários (%s)</a>
        """ % (APPROVAL_PAGE, total_waiting)

    return formatter.rawHTML(html)

# Macro function:
def macro_CommentsAdmin(macro, header_text=u''):
    return CommentsAdmin(macro.request, header_text)
