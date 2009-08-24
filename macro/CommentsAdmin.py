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
    <<CommentsAdmin>>
"""
# General imports:
import os
import glob

# MoinMoin imports:
from MoinMoin import user, wikiutil 
from MoinMoin.Page import Page

class ApproveError(Exception): pass

class CommentsAdmin:
    def __init__(self, macro ):
        self.macro = macro
        
    def get_input( self, arg_name, default = ''  ):
        return wikiutil.escape(
        self.macro.request.form.get(arg_name, [default])[0])

    def get_cfg( self, key, default = None ):
        try:
            return self.macro.request.cfg[key]
        except AttributeError:
            return default

    def render_in_page(self):
        """
        Providing the link to the approval page in any place the user sees fit.
        """
        request = self.macro.request
        
        _ = request.getText
        # Configuration:
        page_name = unicode(self.get_cfg('comment_approval_page',
            'CommentsApproval'))
        page = Page(request,page_name)

        if not page.exists():
            raise ApproveError('You have to create the approval page! (%s)' % (
                    page_name))
        approval_dir = page.getPagePath('', check_create=0)
        approval_url = wikiutil.quoteWikinameURL(page_name)

        formatter = request.html_formatter
        html = ''

        if request.user.isSuperUser():
            # Get the number of comments waiting for approval
            files = glob.glob('%s/*.txt' % approval_dir)
            total_waiting = len(files)

            html = u'<a href="%s">%s (%s)</a>' % (
                approval_url, _('Pending Comments'), total_waiting)

        return formatter.rawHTML(html)

# Macro function:
def macro_CommentsAdmin(macro):
    return CommentsAdmin(macro).render_in_page()