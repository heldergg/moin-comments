# Project #

The aim of this project is to have blog like comments in [MoinMoin](http://moinmo.in/) wiki pages.

This idea isn't new but we could not find an exact implementation of page comments for MoinMoin. What we implement here goes somewhat against the wiki philosophy, but we think that this kind of usage may allow people, that would not otherwise participate on a wiki, to leave their contribution in an easy way.

# Usage #

On this project we define a series of macros that together provide the desired functionality. Currently we have the following macros:

  * **<<AddComment>>** - This macro will display a comment input form. The user input is escaped;

  * **<<ApproveComments>>** - This macro should be placed on the page defined in the configuration variable _comment\_approval\_page_. The comments are temporally stored on this page. The macro will refuse to work on other pages, this allows to use the MoinMoin acl to control the access to this page and thus the moderation;

  * **<<CommentsAdmin>>** - this is an optional macro, it will display how many comments are waiting for moderation - only to the wiki administrators;

  * **<<Comments( PAGE )>>** - This will display the comments available in page _PAGE_.

## Adding and displaying comments ##

For each page where we want to have comments available, we must have at a minimum the AddComment macro somewhere on the page, usually at the end, before the Comments macro:

```
<<AddComment>>
----
<<Comments(@PAGE@)>>
```

This can be placed on the appropriate templates, to automatize the process.

It's easy to block comments in a given page, you only have to edit it and remove the AddComment macro. Likewise, if for instance you have too many comments in a page you can create a sub page and place there the Comments macro. We gain a fairly good amount of flexibility by allowing the usage this way.

## Moderate the comments ##

A page named after the value of the _comment\_approval\_page_ configuration option should be created (_CommentsApproval_ by default). The comments for moderation will be copied to this page.

Somewhere on the page it should be included the _ApproveComments_ macro.

To moderate the comments the site administrator only have to go to this page. Each comment pending moderation will be displayed on this page, ordered by page and date. Besides each comment there are two buttons labeled 'Reject' and 'Accept'.

Please note that the rejected comments are permanently lost.

# Screenshot #

Comment display:

![http://moin-comments.googlecode.com/svn/wiki/img/ricks_comments.png](http://moin-comments.googlecode.com/svn/wiki/img/ricks_comments.png)

Comment creation form:

![http://moin-comments.googlecode.com/svn/wiki/img/add_comment.png](http://moin-comments.googlecode.com/svn/wiki/img/add_comment.png)