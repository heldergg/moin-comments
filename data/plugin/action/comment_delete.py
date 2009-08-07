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
Action Delete Comment

This action deletes a comment.
In the background it deletes the comment file from the for approval directory.
"""
# General imports:
import os
from string import replace, split

# MoinMoin imports:
from MoinMoin.Page import Page

class CommentDelete:
    """
    Aapproves a comment
    """
    def __init__(self, request, referrer):
        # Configuration:
        PAGES_DIR = os.path.join(request.cfg.data_dir, 'pages')
        APPROVAL_PAGE = request.cfg.comment_approval_page
        self.APPROVAL_DIR = os.path.join(PAGES_DIR, APPROVAL_PAGE)

        self.request = request
        self.referrer = referrer
        self.file = self.request.form.get('file', [None])[0]

    def render(self):
        """
        Deletes comment and redirects to the approval page with success message
        """
        # deletes the file text
        os.remove(os.path.join(self.APPROVAL_DIR, self.file))

        # Return Approval page with success message
        msg = u'Comentário Apagado'

        page = Page(self.request, self.referrer)
        self.request.theme.add_msg(msg, "dialog")
        page.send_page()

def execute(pagename, request):
    if request.request_method != 'POST':
        return False, u''
    return CommentDelete(request,pagename).render()
