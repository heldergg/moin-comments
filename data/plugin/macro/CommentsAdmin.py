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
Comments Administration Macro

This macro adds an administration functionality to the comments
feature.
It can be place anywhere, like for instance the wiki menu, and if the
user is a SuperUser he will see the link to the comments approval page,
with the total of comments waiting for approval.

 Usage:
    <<CommentsAdmin()>>
    or
    <<CommentsAdmin(Some header text)>>
"""
# General imports:
import os
import glob
from string import split, replace

# MoinMoin imports:
from MoinMoin import user

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

def CommentsAdmin(request, header_text):
    """
    Providing the link to the approval page in any place the user sees fit.
    """
    formatter = request.html_formatter
    html = ''

    if request.user.isSuperUser():
        if header_text:
            html += '<strong>%s</strong><br /><br />' % header_text

        # Calculate the number of comments waiting for approval
        files = glob.glob('%s/*.txt' % APPROVAL_DIR)
        total_waiting = len(files)

        html += u"""
    <a href="%s">Aprovar Comentários (%s)</a>
        """ % (conf['APPROVAL_PAGE'], total_waiting)

    return formatter.rawHTML(html)

# Macro function:
def macro_CommentsAdmin(macro, header_text=u''):
    return CommentsAdmin(macro.request, header_text)
