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
Action Add Comment
By José Lopes - Bombolom.com

This action creates a new comment from the form passed by the
AddComments macro, and saves it under the APPROVAL_PAGE.

Mandatory:
    - The APPROVAL_PAGE must exist and be declared on the constants
    - The Comments page must exist for the page in question
"""

# General imports:
from datetime import datetime
import os
from string import replace, split, letters, digits
from random import choice

# MoinMoin imports:
from MoinMoin import config
from MoinMoin.Page import Page
from MoinMoin import wikiutil

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

pages_dir = os.path.join(os.path.split(os.path.split(current_dir)[0])[0], 'pages')
APPROVAL_DIR = os.path.join(pages_dir, conf['APPROVAL_PAGE'])

class AddComment:
    """
    Add a comment to the approval list.
    """
    def __init__(self, request, referrer):
        self.request = request

        self.page = self.request.form.get('page', [None])[0]
        self.user_name = wikiutil.escape(
                            self.request.form.get('user_name', [None])[0] )
        self.comment = wikiutil.escape(
                            self.request.form.get('comment', [None])[0] )
        self.email = wikiutil.escape(
                            self.request.form.get('email', [None])[0] )
        self.date = datetime.now()

    def errors_check(self):
        """
        Check the form for errors.
        """
        if not self.user_name:
            return u'O seu nome é obrigatório'
        if not self.comment:
            return u'Ainda não escreveu qualquer comentário'
        return ''

    def write_comment_for_approval(self):
        """
        Writes the comment to the approval directory for evaluation.
        """
        moment = self.date
        page_ref = replace(self.page, '/', '_')

        comment_hash =  ''.join([choice(letters + digits) for i in range(20)])

        comment_file = '%s-%s%s.txt' % (page_ref, int(moment.strftime("%s")), comment_hash)

        info = u"""<p id="comment_header">%s - Por <b>%s</b><p>%s</p>""" % (
                moment.strftime("%d-%m-%Y %H:%M:%S"),
                self.user_name,
                self.comment)

        file = open(os.path.join(APPROVAL_DIR, comment_file), 'wb')
        file.write(info.encode('utf-8'))
        file.close()

    def render(self):
        """
        Redirect to the comment page if success.
        """
        error = self.errors_check()

        if error:
            # Send back to the page you came from, with an error msg
            page = Page(self.request, self.page)
            self.request.theme.add_msg(error, "error")
            page.send_page()
        else:

            self.write_comment_for_approval()

            pagename = '%s' % self.page
            msg = u'O seu comentário aguarda moderação'

            page = Page(self.request, pagename)
            self.request.theme.add_msg(msg, "dialog")
            page.send_page()

def execute(pagename, request):
    if request.request_method != 'POST':
        return False, u''
    return AddComment(request,pagename).render()
