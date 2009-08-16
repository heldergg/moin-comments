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
Add Comment Macro

This macro places the comment form on the page.

Usage:
    <<AddComment(Add a Comment title, Add button label)>>
"""

# MoinMoin imports:
from MoinMoin import wikiutil
from MoinMoin.Page import Page

from datetime import datetime
from random import choice
from string import letters, digits
import pickle
import os

# Auxiliary class:
class AddComment:
    def __init__(self, macro ):
        self.macro = macro
        self.page_name = macro.formatter.page.page_name

        self.msg = ''
        self.comment = {
                'user_name' : '',
                'comment': '',
                'email': '',
                }
        self.errors = []

        if macro.request.request_method == 'POST':
            self.save_comment()

    def get_input( self, arg_name, default = ''  ):
        return wikiutil.escape(
                self.macro.request.form.get(arg_name, [default])[0])

    def get_cfg( self, key, default = None ):
        try:
            return self.macro.request.cfg[key]
        except AttributeError:
            return default

    def get_comment(self):
        self.comment = {
            'user_name' : self.get_input('user_name'),
            'comment': self.get_input('comment'),
            'email': self.get_input('email'),
            }

    def errors_check(self):
        """
        Check the form for errors.
        """
        _ = self.macro.request.getText

        errors = []

        if not self.comment['user_name']:
            errors.append( _('You must enter your name.') )
        if len(self.comment['user_name']) > 128:
            errors.append( _('Please use a shorter name.') )
        if not self.comment['comment']:
            errors.append( _('You have yet to write your comment.') )
        if len(self.comment['comment']) > 10240:
            errors.append( _('Maximum number of characters is 10240.'))
            
        if ( self.get_cfg('comment_recaptcha', False) and
            not self.captcha.is_valid ):
            errors.append( _("I'm not sure you're human! Please fill in the captcha."))
            
        return errors

    def save_comment( self ):
        _ = self.macro.request.getText
        
        if self.get_input( 'do' ) != u'comment_add':
            # This is not a comment post do nothing
            return

        if self.get_cfg('comment_recaptcha', False ):
            import captcha
            self.captcha = captcha.submit (
                get_arg('recaptcha_challenge_field'),
                get_arg('recaptcha_response_field'),
                self.get_cfg('comment_recaptcha_private_key'),
                request.remote_addr )

        self.get_comment()
        self.errors = self.errors_check()

        if not self.errors: # Save the comment
            # Find out where to save the comment:
            if self.get_cfg('comment_moderate', True):
                page = Page(self.macro.request,
                    self.get_cfg('comment_approval_page', 'CommentsApproval'))
                comment_dir = page.getPagePath('', check_create=0)
            else:
                page = Page(self.macro.request,self.page_name)
                comment_dir = page.getPagePath('comments', check_create=1)

            now = datetime.now()
            random_str =  ''.join([choice(letters + digits) for i in range(20)])
            comment_file = '%s-%s.txt' % (now.strftime("%s"), random_str)
            file_name = os.path.join(comment_dir, comment_file)

            comment = self.comment
            comment['page'] = self.page_name
            comment['time'] = now
            if self.get_cfg('comment_store_addr', False):
                comment['remote_addr'] = self.macro.request.remote_addr

            f = open(file_name, 'wb')
            pickle.dump(comment, f )
            f.close()

            if self.get_cfg('comment_moderate', True):
                self.msg = _('Your comment awaits moderation. Thank you.')
            else:
                self.msg = _('Your comment has been posted. Thank you.')
                
            # clean up the fields to display
            self.comment = {
                'user_name' : '',
                'comment': '',
                'email': '',
                }

    def renderInPage(self):
        """
        Render comments form in page context.
        """
        _ = self.macro.request.getText
        html = u'''<div class="comments_form">
        <form method="POST" action="%(page_uri)s">
        <input type="hidden" name="do" value="comment_add">
        <table>''' % { 'page_uri': self.macro.request.request_uri }

        html += '''
            <tr>
                <td colspan=2 id="center_cell"><b>%(header)s</b></td>
            </tr>
            <tr>
                <th>%(name_label)s</th>
                <td>
                    <input type="text" id="name" maxlength=128 name="user_name"
                           value="%(user_name)s">
                </td>
            </tr>
            <tr>
                <th>%(comment_label)s</th>
                <td>
                    <textarea name="comment">%(comment)s</textarea>
                </td>
            </tr>
            ''' % {
            'page_name': self.page_name,
            'user_name': self.comment['user_name'],
            'comment':   self.comment['comment'],
            'header': _('Comment this page'),
            'name_label': _('Name:'),
            'comment_label': _('Comment:')  }

        if self.msg:
            html += u'<tr><td colspan = 2><div id="comment_message">'
            html += u'<p>%s</p>' % self.msg
            html += u'</div></td></tr>'

        if self.errors:
            html += u'<tr><td colspan = 2><div id="comment_error">'
            if len(self.errors) > 1:
                html += u'<p>%s</p><ul>'  % _('Your comment has errors:')
            else:
                html += u'<p>%s</p><ul>'  % _('Your comment has one error:')
            for error in self.errors:
                html += u'<li>%s</li>' % error
            html += u'</ul></div></td></tr>'

        if self.get_cfg('comment_recaptcha', False):
            import captcha
            html += u"""
            <tr>
                <th>%(recaptcha_label)s</th>
                <td>%(recaptcha)s</td>
            </tr>""" % {
            'recaptcha' : captcha.displayhtml(
                                self.get_cfg('comment_recaptcha_public_key')),
            'recaptcha_label': _('Are you human?') }

        html += """
             <tr>
                <td colspan=2 id="center_cell"><input type="submit" value="%(label)s">
                </td>
            </tr>
        </table></form></div>""" % { 'label': _('Send comment') }

        return self.macro.formatter.rawHTML(html)

# Macro function:
def macro_AddComment(macro):
    return AddComment(macro).renderInPage()
