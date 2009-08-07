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
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        if header:
            self.header = header
        else:
            self.header = u'Comentar esta página'

        if button_label:
            self.label = button_label
        else:
            self.label = u'Enviar Comentário'

    def renderInPage(self):
        """
        Render comments form in page context.
        """

        html = u"""
<center>
<div class="comments_form">
    <form method="POST" action="%s">
        <input type="hidden" name="action" value="comment_add">
        <input type="hidden" name="page" value="%s">
        <table>
             <tr>
                <td></td>
                <td id="center_cell"><b>%s</b></td>
            </tr>
            <tr>
                <th>Nome:</th>
                <td>
                    <input type="text" id="name" name="user_name">
                </td>
            </tr>
            <tr>
                <th>Comentário:</th>
                <td>
                    <textarea name="comment"></textarea>
                </td>
            </tr>
            <tr>
                <td></td>
                <td id="center_cell"><input type="submit" value="%s"></td>
            </tr>
        </table>
    </form>
</div>
</center>
                """ % (wikiutil.quoteWikinameURL(self.formatter.page.page_name),
                    wikiutil.quoteWikinameURL(self.formatter.page.page_name),
                    wikiutil.escape(self.header, 1),
                    wikiutil.escape(self.label, 1))

        return self.formatter.rawHTML(html)

# Macro function:
def macro_AddComment(macro, header=u'', button_label=u''):
    return AddComment(macro, header, button_label).renderInPage()
