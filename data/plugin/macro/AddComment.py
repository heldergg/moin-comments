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

# Auxiliary class:
class AddComment:
    def __init__(self, macro, header=u'', button_label=u''):
        def get_arg( arg_name ):
            return wikiutil.escape(self.request.form.get(arg_name, [''])[0])

        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter

        _ = self.request.getText

        if header:
            self.header = header
        else:
            self.header = _('Comment this page')

        if button_label:
            self.label = button_label
        else:
            self.label = _('Send comment')

        # If there where errors we've to redisplay the user input:
        self.user_name = get_arg('user_name')
        self.comment = get_arg('comment')
        self.email = get_arg('email')

    def renderInPage(self):
        """
        Render comments form in page context.
        """
        _ = self.request.getText
        html = u"""
<center>
<div class="comments_form">
    <form method="POST" action="/%(page_name)s">
        <input type="hidden" name="action" value="comment_add">
        <input type="hidden" name="page" value="%(page_name)s">
        <table>
            <tr>
                <td></td>
                <td id="center_cell"><b>%(header)s</b></td>
            </tr>
            <tr>
                <th>%(name_label)s</th>
                <td>
                    <input type="text" id="name" maxlength=128 name="user_name" value="%(user_name)s">
                </td>
            </tr>
            <tr>
                <th>%(comment_label)s</th>
                <td>
                    <textarea name="comment">%(comment)s</textarea>
                </td>
            </tr>
            """ % {
        'page_name': self.formatter.page.page_name,
        'header': wikiutil.escape(self.header, 1),
        'user_name': self.user_name,
        'comment': self.comment,
        'name_label': _('Name:'),
        'comment_label': _('Comment:')  }

        if self.request.cfg.comment_recaptcha:
            import captcha
            html += u"""
            <tr>
                <th>%(recaptcha_label)s</th>
                <td>
                    %(recaptcha)s
                </td>
            </tr>""" % {

            'recaptcha' : captcha.displayhtml(
                                self.request.cfg.comment_recaptcha_public_key ),
            'recaptcha_label': _('Are you human?') }

        html += """
             <tr>
                <td></td>
                <td id="center_cell"><input type="submit" value="%(label)s">
                </td>
            </tr>
        </table>
    </form>
</div>
</center>""" % { 'label': wikiutil.escape(self.label, 1) }

        return self.formatter.rawHTML(html)

# Macro function:
def macro_AddComment(macro, header=u'', button_label=u''):
    return AddComment(macro, header, button_label).renderInPage()
