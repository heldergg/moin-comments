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
Comments Macro

This macro display the comments page.
It collects the comments files and displays its content.

Usage:
    <<Comments(@PAGE@)>> on the Comments page
"""

# General imports:
import os
import glob
import pickle
from string import letters, digits
from random import choice

# MoinMoin imports
from MoinMoin.Page import Page
from MoinMoin import wikiutil

def read_comment( file_name ):
    f = open(file_name, 'r')
    comment = pickle.load(f)
    f.close()
    return comment

# Auxiliary function:
class Comments:
    def __init__(self, macro, page_name):
        self.macro = macro
        
        if page_name == u'':
            # By default show the comments for the current page
            page_name = macro.formatter.page.page_name
        self.page_name = page_name

    def get_input( self, arg_name, default = ''  ):
        return wikiutil.escape(
                self.macro.request.form.get(arg_name, [default])[0])

    def get_cfg( self, key, default = None ):
        try:
            return self.macro.request.cfg[key]
        except AttributeError:
            return default


    def comment_html(self, comment):
        _ = self.macro.request.getText
        return '''<table>
    <tr><td>%(name)s</td><td>%(comment_name)s</td></tr>
    <tr><td>%(time)s</td><td>%(comment_time)s</td></tr>
    <tr><td colspan=2>%(comment_text)s</td></tr>
    </table>''' % {
        'name': _('Name:'),
        'comment_name': comment['user_name'],
        'time': _('Time:'),
        'comment_time': comment['time'].strftime('%Y.%m.%d %H:%M'),
        'comment_text': '<p>'.join( comment['comment'].split('\n') ),
        }

    def render_in_page(self):
        """
        Returns comments in page context.
        """
        _ = self.macro.request.getText
        
        def navbar(page_number, max_pages, page_uri):
            if max_pages == 1:
                return ''
            
            html = ['<div class="navbar">']
            if page_number > 1:
                html.append('<div class="prevcmt">')
                html.append('<a href="http://%s">%s</a>&nbsp;&nbsp;&nbsp;' %
                        (page_uri,_('|&lt;')))
                html.append('<a href="http://%s?page_number=%d">%s</a>&nbsp;&nbsp;&nbsp;' %
                        (page_uri,page_number-1,_('&lt;&lt;')))
                html.append('</div>')
            
            if page_number < max_pages:
                html.append('<div class="nextcmt">')
                html.append('<a href="http://%s?page_number=%d">%s</a>&nbsp;&nbsp;&nbsp;' %
                        (page_uri,page_number+1,_('&gt;&gt;')))
                html.append('<a href="http://%s?page_number=%d">%s</a>&nbsp;&nbsp;&nbsp;' %
                        (page_uri,max_pages,_('&gt;|')))
                html.append('</div>')

            html.append('</div>')

            return '\n'.join(html)
            
        # Get the configuration:

        page = Page(self.macro.request, self.page_name )
        comments_dir = page.getPagePath("comments", check_create=1)

        files = glob.glob(os.path.join(comments_dir,'*.txt'))
        files.sort()

        html = [u'<a name="comment_section"></a>']
        if not files:
            html.append(u'<p>%s</p>' % _('There are no comments'))
        else:
            # Do the pagination
            cmt_per_page = int(self.get_cfg('comment_cmt_per_page',50))

            if cmt_per_page:
                page_uri = self.macro.request.splitURI(self.macro.request.url)[0]

                number_messages = len(files)
                max_pages = ( number_messages / cmt_per_page +
                            (1 if number_messages % cmt_per_page else 0 ))
                try:
                    page_number = int(self.get_input( 'page_number', 1 ))
                except ValueError:
                    page_number = 1
                if page_number > max_pages:
                    page_number = max_pages
                elif page_number < 1:
                    page_number = 1

                first = (page_number - 1) * cmt_per_page
                last  = first + cmt_per_page

                files = files[first:last]
            
            # Get the file names
            comments = [ read_comment(Xi) for Xi in files]

            for comment in comments:
                html.append( u"%s" % self.comment_html( comment ) )

            if cmt_per_page:
                html.append(navbar(page_number, max_pages, page_uri))

        return self.macro.request.html_formatter.rawHTML('\n'.join(html))

# Macro function:
def macro_Comments(macro, page_name=u''):
    return Comments(macro, page_name).render_in_page()
