# -*- coding: utf-8 -*-

# Moin-comments - Blog like comments in MoinMoin
# Copyright (C) 2009, 2017 José Lopes

# This file is part of Moin-comments.
#
# Moin-comments is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Moin-comments is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Moin-comments.  If not, see <http://www.gnu.org/licenses/>.

#
# José Lopes <jose.lopes@tretas.org>
# Helder Guerreiro <helder@tretas.org>
#


"""
Add Comment Macro

This macro places the comment form on the page.

Usage:
    <<AddComment>>
"""

# MoinMoin imports:
from MoinMoin.Page import Page
from MoinMoin.mail import sendmail
from MoinMoin.datastruct.backends import GroupDoesNotExistError

from datetime import datetime
from random import choice
from string import letters, digits

import platform
import os

# Necessary to check the recaptcha response
import urllib
import urllib2
import json

from comment_utils import get_cfg, get_input, write_comment, notify_subscribers

# Auxiliary class:


class AddComment:

    def __init__(self, macro):
        self.macro = macro
        self.page = macro.request.page
        self.user = macro.request.user
        self.page_name = macro.formatter.page.page_name

        self.msg = ''
        self.reset_comment()
        self.errors = []

        try:
            passpartout_group = macro.request.groups[
                get_cfg(macro, 'comment_passpartout_group', 'PasspartoutGroup')]

            if self.user.name in passpartout_group:
                passpartout = True
            else:
                passpartout = False
        except GroupDoesNotExistError:
            passpartout = False

        self.passpartout = passpartout
        self.moderate = get_cfg(
            macro, 'comment_moderate', True) and not passpartout

        # Check if the user can create new comments:
        only_logged = get_cfg(self.macro, 'comment_only_logged', False)
        follow_acl = get_cfg(self.macro, 'comment_follow_acl', False)
        may_write = self.user.may.write(self.page_name)

        self.can_create = ((not follow_acl or (follow_acl and may_write)) and
                           (not only_logged or self.user.exists()))

        # Save the comment
        if macro.request.method == 'POST' and self.can_create:
            self.save_comment()

    def reset_comment(self):
        '''Resets the comment dict to default a value'''
        self.comment = {
            'user_name': self.user.name,
            'comment': '',
            'email': '',
        }

    def get_comment(self):
        self.comment = {
            'user_name': get_input(self.macro, 'user_name'),
            'comment': get_input(self.macro, 'comment'),
            'email': get_input(self.macro, 'email'),
        }

    def errors_check(self):
        """
        Check the form for errors.
        """
        _ = self.macro.request.getText

        errors = []

        if not self.comment['user_name']:
            errors.append(_('You must enter your name.'))
        if len(self.comment['user_name']) > 128:
            errors.append(_('Please use a shorter name.'))
        if not self.comment['comment']:
            errors.append(_('You have yet to write your comment.'))
        if len(self.comment['comment']) > 10240:
            errors.append(_('Maximum number of characters is 10240.'))

        if (get_cfg(self.macro, 'comment_recaptcha', False) and not self.passpartout
                and not self.captcha_is_valid):
            errors.append(
                _("I'm not sure you're human! Please fill in the captcha."))

        return errors

    def save_comment(self):
        _ = self.macro.request.getText

        if get_input(self.macro, 'do') != u'comment_add':
            # This is not a comment post do nothing
            return

        if get_cfg(self.macro, 'comment_recaptcha', False) and not self.passpartout:
            self.captcha_is_valid = False
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                    'secret': get_cfg(self.macro, 'comment_recaptcha_private_key'),
                    'response': get_input(self.macro, 'g-recaptcha-response'),
                    'remoteip': self.macro.request.remote_addr,
                    }
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.load(response)
            self.captcha_is_valid = result['success']

        self.get_comment()
        self.errors = self.errors_check()

        if not self.errors:  # Save the comment
            # Find out where to save the comment:
            if self.moderate:
                # This commet will be added to the moderation queue
                page = Page(self.macro.request,
                            get_cfg(self.macro, 'comment_approval_page', 'CommentsApproval'))
                comment_dir = page.getPagePath('', check_create=0)
            else:
                # The comment will be immediately posted
                page = Page(self.macro.request, self.page_name)
                comment_dir = page.getPagePath('comments', check_create=1)

            # Compose the comment structure and write it
            now = datetime.now()
            if platform.system() == 'Windows':
                # Windows doesn't return seconds since epoch, because of this the
                # comments are unordered on this platform. To fix this I'll
                # calculate the number of seconds since the unix epoch on windows
                # this way the comment file names are consistent and interchangeable
                # between platforms.
                td = now - datetime(1970, 1, 1, 0, 0)
                seconds = '%d' % (td.seconds + td.days * 24 * 3600 - 3600)
            else:
                seconds = now.strftime("%s")

            random_str = ''.join([choice(letters + digits) for i in range(20)])
            comment_file = '%s-%s.txt' % (seconds, random_str)
            file_name = os.path.join(comment_dir, comment_file)

            comment = self.comment
            comment['page'] = self.page_name
            comment['time'] = now
            if get_cfg(self.macro, 'comment_store_addr', False):
                comment['remote_addr'] = self.macro.request.remote_addr

            if self.moderate:
                self.msg = _('Your comment awaits moderation. Thank you.')
            else:
                self.msg = _('Your comment has been posted. Thank you.')

            write_comment(file_name, comment)

            if self.moderate:
                # If we have defined a list of moderators to notify and this user is
                # moderated then a message is sent to the moderator list
                moderators = get_cfg(self.macro, 'comment_moderators', None)
                if moderators:
                    sendmail.sendmail(self.macro.request, moderators.split(','),
                                      _('New comment awaits moderation for page %(page)s' %
                                        self.comment),
                                      _('New comment awaits moderation:\n\n'
                                        'Page: %(page)s\nFrom: %(user_name)s'
                                        '\nMessage:\n\n%(comment)s\n\n--' %
                                        self.comment))
            else:
                # Send notification to page subscribers if the page
                notify_subscribers(self.macro, self.comment)

            # clean up the fields to display
            self.reset_comment()

    def get_html(self):
        """
        Generate the comment form
        """
        _ = self.macro.request.getText
        html = u'<div class="comments_form">'

        if get_cfg(self.macro, 'comment_recaptcha', False) and not self.passpartout:
            html += '<script src="https://www.google.com/recaptcha/api.js" async defer></script>\n'

        html += u'''
        <form method="POST" action="%(page_uri)s">
        <input type="hidden" name="do" value="comment_add">
        <table>''' % { 'page_uri': self.macro.request.request.url }

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
            'comment_label': _('Comment:')}

        if self.msg:
            html += u'<tr><td colspan = 2><div id="comment_message">'
            html += u'<p>%s</p>' % self.msg
            html += u'</div></td></tr>'

        if self.errors:
            html += u'<tr><td colspan = 2><div id="comment_error">'
            if len(self.errors) > 1:
                html += u'<p>%s</p><ul>' % _('Your comment has errors:')
            else:
                html += u'<p>%s</p><ul>' % _('Your comment has one error:')
            for error in self.errors:
                html += u'<li>%s</li>' % error
            html += u'</ul></div></td></tr>'

        if get_cfg(self.macro, 'comment_recaptcha', False) and not self.passpartout:
            html += u"""
            <tr>
                <th>%(recaptcha_label)s</th>
                <td><div class="g-recaptcha" data-sitekey="%(recaptcha)s"></div></td>
            </tr>""" % {
                'recaptcha': get_cfg(self.macro, 'comment_recaptcha_public_key'),
                'recaptcha_label': _('Are you human?')}

        html += """
             <tr>
                <td colspan=2 id="center_cell"><input type="submit" value="%(label)s">
                </td>
            </tr>
        </table></form></div>""" % { 'label': _('Send comment') }

        return html

    def renderInPage(self):
        """
        Render comments form in page context.
        """
        # Comments restricted to logged-in users

        if self.can_create:
            return self.macro.formatter.rawHTML(self.get_html())
        else:
            return self.macro.formatter.escapedText('')


# Macro function:
def macro_AddComment(macro):
    return AddComment(macro).renderInPage()
