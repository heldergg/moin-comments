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
Approve Comments Macro

This macro lists the comments waiting for approval and displays the
delete and approval buttons.

Usage:
    <<ApproveComments()>>

Requirements:
    You must define the correct path at WORK_DIR
"""

# General imports:
import os
from string import split, replace
import glob

# Get the configuration values
conf = {}
current_dir =  os.path.dirname(__file__)
conf_file = os.path.join(current_dir, 'comments_config.txt')

data = open(conf_file, 'r')
lines = data.readlines()
data.close()
for line in lines:
    line = replace(line, '\n', '')
    line = split(line, '==')
    conf[line[0]]=line[1]

pages_dir = os.path.join(os.path.split(os.path.split(current_dir)[0])[0], 'pages')
APPROVAL_DIR = os.path.join(pages_dir, conf['APPROVAL_PAGE'])

# Auxiliary function:
def ApproveComments(request):
    """
    Render comments form in page context.
    """
    formatter = request.html_formatter
    html = ''

    files = glob.glob('%s/*.txt' % APPROVAL_DIR)

    if not files:
        html = u'<p>Não existe nenhum comentário à espera de moderação</p>'
    else:
        # Organize files by page
        info = {}
        for file in files:
            file = split(file, '/')
            title = split(file[-1], '-')
            if not info.has_key(title[0]):
                info[title[0]] = []
            info[title[0]].append(title[1])

        for key in info:
            comments = info[key]
            comments.sort()
            comments.reverse()

            for comment in comments:

                data = open(os.path.join(APPROVAL_DIR, '%s-%s' % (key, comment)), 'r')
                lines = data.read().decode('utf-8')
                data.close()

                if lines:
                    html += u"""
<div class="comment_approval">
<table>
    <tr>
        <th>Comentário a %s</th>
    </tr>
    <tr>
        <td>%s</td>
    </tr>
    <tr>
        <td>
            <form method="POST" action="/CommentsApproval">
            <input type="hidden" name="action" value="comment_delete">
            <input type="submit" value="Apagar" id="delete">
            <input type="hidden" name="file" value="%s-%s">
            </form>
            <form method="POST" action="/CommentsApproval">
            <input type="hidden" name="action" value="comment_approve">
            <input type="submit" value="Aceitar" id="ok">
            <input type="hidden" name="file" value="%s-%s">
            </form>
        </td>
    </tr>
</table>
</div><br />
            """ % (replace(key,'_','\\'), lines, key, comment, key, comment)

                else: # If the file is empty:
                    html += u"""
<div class="comment_approval">
<table>
    <tr>
        <th colspan=2>Comentário a %s</th>
    </tr>
    <tr>
        <td>Comentário vazio. Deve ser apagado!</td>
        <td>
            <form method="POST" action="/CommentsApproval">
            <input type="hidden" name="action" value="comment_delete">
            <input type="submit" value="Apagar">
            <input type="hidden" name="file" value="%s-%s">
            </form>
        </td>
    </tr>
</table>
</div><br />
            """ % (replace(key,'_','\\'), key, comment)

    return formatter.rawHTML(html)

# Macro function:
def macro_ApproveComments(macro):
    return ApproveComments(macro.request)
