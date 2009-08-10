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
Action Approve Comment

This action approves a comment.
In the background it moves the comment file from the
for approval directory to the correct page comments
directory.
"""

# General imports:
import os
from string import replace, split

# MoinMoin imports:
from MoinMoin.Page import Page

class CommentApprove:
    """
    Aapproves a comment
    """
    def __init__(self, request, referrer):
        # TODO: use the following method to get the page dir, it will not
        # fail with non ascii chars on the page name.
        page = Page(request, request.cfg.comment_approval_page )
        self.APPROVAL_DIR = page.getPageBasePath()[1]

        self.request = request
        self.referrer = referrer

        self.origin = self.request.form.get('file', [''])[0]

        page_name = self.request.form.get('page_name', [''])[0]
        page = Page(request, page_name )
        dest_dir = page.getPagePath("comments", check_create=1)

        self.destination = os.path.join(dest_dir,os.path.basename(self.origin))

    def render(self):
        """
        Approves comment and redirects to the approval page with success message
        """
        _ = self.request.getText

        # Move the file text
        os.rename(self.origin, self.destination)

        # Return Approval page with success message
        msg = _('Comment approved')

        page = Page(self.request, self.referrer)
        self.request.theme.add_msg(msg, "dialog")
        page.send_page()

def execute(pagename, request):
    if request.request_method != 'POST':
        return False, u''
    return CommentApprove(request,pagename).render()
