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

# Get the configuration values
conf = {}
current_dir =  os.path.dirname(__file__)
config_dir = os.path.join(os.path.split(current_dir)[0], 'macro')
conf_file = os.path.join(config_dir, 'comments_config.txt')

data = open(conf_file, 'r')
lines = data.readlines()
data.close()
for line in lines:
    line = replace(line, '\n', '')
    line = split(line, '==')
    conf[line[0]]=line[1]

PAGES_DIR = os.path.join(os.path.split(os.path.split(current_dir)[0])[0], 'pages')
APPROVAL_DIR = os.path.join(PAGES_DIR, conf['APPROVAL_PAGE'])

class CommentApprove:
    """
    Aapproves a comment
    """
    def __init__(self, request, referrer):
        self.request = request
        self.referrer = referrer
        self.file = self.request.form.get('file', [None])[0]

    def render(self):
        """
        Approves comment and redirects to the approval page with success message
        """
        # Move the file text
        origin = os.path.join(APPROVAL_DIR, self.file)

        page_dest = split(self.file, '-')
        dir_dest = replace(page_dest[0],  '_',  '(2f)')

        # Rename the file (no need for the page name any more)
        new_file_name = page_dest[1]

        destination_dir = os.path.join(PAGES_DIR, dir_dest, 'comments' )
        destination = os.path.join( destination_dir, new_file_name)

        if not os.path.exists( destination_dir ):
            os.mkdir( destination_dir )

        os.rename(origin, destination)

        # Return Approval page with success message
        msg = u'Comentário Approvado'

        page = Page(self.request, self.referrer)
        self.request.theme.add_msg(msg, "dialog")
        page.send_page()

def execute(pagename, request):
    if request.request_method != 'POST':
        return False, u''
    return CommentApprove(request,pagename).render()
