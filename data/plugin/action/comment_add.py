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
Action Add Comment

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

class AddComment:
    """
    Add a comment to the approval list.
    """
    def __init__(self, request, referrer):

        # Configuration:
        PAGES_DIR = os.path.join(request.cfg.data_dir, 'pages')
        APPROVAL_PAGE = request.cfg.comment_approval_page
        self.APPROVAL_DIR = os.path.join(PAGES_DIR, APPROVAL_PAGE)

        self.request = request
        self.page = self.request.form.get('page', [None])[0]
        self.user_name = wikiutil.escape(
                            self.request.form.get('user_name', [None])[0] )
        self.comment = wikiutil.escape(
                            self.request.form.get('comment', [None])[0] )
        self.email = wikiutil.escape(
                            self.request.form.get('email', [None])[0] )
        self.date = datetime.now()
        if request.cfg.comment_recaptcha:
            import captcha
            self.captcha = captcha.submit (
                self.request.form.get('recaptcha_challenge_field', [None])[0],
                self.request.form.get('recaptcha_response_field', [None])[0],
                request.cfg.comment_recaptcha_private_key,
                request.remote_addr )

    def errors_check(self):
        """
        Check the form for errors.
        """
        _ = self.request.getText

        if not self.user_name:
            return _('You must enter your name.')
        if not self.comment:
            return _('You have yet to write your comment.')
        if ( self.request.cfg.comment_recaptcha and
            not self.captcha.is_valid ):
            return _("I'm not sure you're human! Please fill in the captcha." )
        return ''

    def write_comment_for_approval(self):
        """
        Writes the comment to the approval directory for evaluation.
        """
        _ = self.request.getText
        moment = self.date
        page_ref = replace(self.page, '/', '_')

        comment_hash =  ''.join([choice(letters + digits) for i in range(20)])

        comment_file = '%s-%s%s.txt' % (page_ref, int(moment.strftime("%s")),
                    comment_hash)

        info = '<p id="comment_header">%(time)s - %(by)s <b>%(user_name)s</b><p>%(comment)s</p>' % {
                'time': moment.strftime("%d-%m-%Y %H:%M:%S"),
                'user_name': self.user_name,
                'comment': self.comment,
                'by': _('Comment by') }

        file = open(os.path.join(self.APPROVAL_DIR, comment_file), 'wb')
        file.write(info.encode('utf-8'))
        file.close()

    def render(self):
        """
        Redirect to the comment page if success.
        """
        error = self.errors_check()
        _ = self.request.getText

        if error:
            # Send back to the page you came from, with an error msg
            page = Page(self.request, self.page)
            self.request.theme.add_msg(error, "error")
            page.send_page()
        else:
            self.write_comment_for_approval()

            self.request.form['user_name'] = ['']
            self.request.form['comment'] = ['']
            self.request.form['email'] = ['']

            pagename = '%s' % self.page
            msg = _('Your comment awaits moderation')

            page = Page(self.request, pagename)
            self.request.theme.add_msg(msg, "dialog")
            page.send_page()

def execute(pagename, request):
    if request.request_method != 'POST':
        return False, u''
    return AddComment(request,pagename).render()
