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
"""

# General imports:
from datetime import datetime
import os
from string import replace, split, letters, digits
from random import choice
import pickle

# MoinMoin imports:
from MoinMoin import config
from MoinMoin.Page import Page
from MoinMoin import wikiutil

class CommentError(Exception): pass

class AddComment:
    """
    Add a comment to the approval list.
    """
    def __init__(self, request, referrer):
        def get_arg( arg_name ):
            return wikiutil.escape(self.request.form.get(arg_name, [''])[0])


        # Configuration:
        PAGES_DIR = os.path.join(request.cfg.data_dir, 'pages')
        APPROVAL_PAGE = request.cfg.comment_approval_page
        self.APPROVAL_DIR = os.path.join(PAGES_DIR, APPROVAL_PAGE)

        # Read the form
        self.request = request
        self.page = get_arg('page')
        self.user_name = get_arg('user_name')
        self.comment = get_arg('comment')
        self.email = get_arg('email')
        self.date = datetime.now()

        if request.cfg.comment_recaptcha:
            import captcha
            self.captcha = captcha.submit (
                get_arg('recaptcha_challenge_field'),
                get_arg('recaptcha_response_field'),
                request.cfg.comment_recaptcha_private_key,
                request.remote_addr )

    def errors_check(self):
        """
        Check the form for errors.
        """
        _ = self.request.getText

        if not self.user_name:
            return _('You must enter your name.')
        if len(self.user_name) > 128:
            return _('Please use a shorter name.')
        if not self.comment:
            return _('You have yet to write your comment.')
        if len(self.comment) > 10240:
            return _('Maximum number of characters is 10240.')
        if ( self.request.cfg.comment_recaptcha and
            not self.captcha.is_valid ):
            return _("I'm not sure you're human! Please fill in the captcha.")
        return ''

    def write_comment_for_approval(self):
        """
        Writes the comment to the approval directory for evaluation.
        """
        _ = self.request.getText

        random_str =  ''.join([choice(letters + digits) for i in range(20)])
        comment_file = '%s-%s.txt' % (self.date.strftime("%s"), random_str)
        file_name = os.path.join(self.APPROVAL_DIR, comment_file)

        comment = {}
        comment['page'] = self.page
        comment['time'] = self.date
        comment['email'] = self.email
        comment['user_name'] = self.user_name
        comment['comment'] = self.comment

        f = open(file_name, 'wb')
        pickle.dump(comment, f )
        f.close()

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

            msg = _('Your comment awaits moderation')

            page = Page(self.request, self.page)
            self.request.theme.add_msg(msg, "dialog")
            page.send_page()

def execute(pagename, request):
    if request.request_method != 'POST':
        return False, u''
    return AddComment(request,pagename).render()

