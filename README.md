# Project Objective

The aim of this project is to have blog like comments in MoinMoin wiki blog pages.

This idea isn't new but we could not find an exact implementation of page comments for MoinMoin. What we implement here goes somewhat against the wiki philosophy, but we think that this kind of usage may allow people that would not otherwise participate on a wiki leave their contribution in an easy and fast way.

# Usage

On this project we define a series of actions and macros that together provide the described functionality. For the user, the actions usage is transparent, he will only have to care of the macros:

* `<<AddComment>>` - This macro will display a comment input form. The user input is escaped so if the user types some markup it will not produce any effect;

* `<<ApproveComments>>` - This macro should be placed on the page defined in the configuration variable `comment_approval_page`. The comments are temporally stored on this page. A site administrator must moderate the comments;

* `<<CommentsAdmin>>` - this is an optional macro, it will display how many comments are waiting for moderation - only to the wiki administrators;

* `<<Comments(PAGE)>>` - This will display the comments available in page `PAGE`.

## Adding and displaying comments

For each page where we want to have comments available, we must have at a minimum the AddComment macro somewhere on the page, usually at the end, before the Comments macro:

```
<<AddComment>>
----
<<Comments(@PAGE@)>>
```

This can be placed on the appropriate templates, to automatize the process.

It's easy to block comments in a given page, you only have to edit it and remove the AddComment macro. Likewise, if for instance you have too many comments in a page you can create a sub page and place there the Comments macro. We gain a fairly good amount of flexibility by allowing the usage this way.

## Moderate the comments

A page named after the value of the `comment_approval_page` configuration option should be created (`CommentsApproval` by default). The comments for moderation will be copied to this page.

Somewhere on the page it should be included the `ApproveComments` macro.

To moderate the comments the site administrator only have to go to this page. Each comment pending moderation will be displayed on this page, ordered by page and date. Besides each comment there are two buttons labeled 'Reject' and 'Accept'.

Please note that the rejected comments are permanently lost.

# Configuration options

You may define on your wiki configuration the following options:

| **Option**                    | **Description** |
|:------------------------------|:----------------|
| comment\_moderate            | (Default: True) If enabled the comments will be copied to a moderation queue and have to be accepted/rejected by a moderator |
| comment\_moderators          | (Default: None) If defined this should contain a comma separated list of email addresses. If a comment is to be moderated and this is defined, a message will be sent to the listed email addresses. |
| comment\_template | (Default: `<Defined in Comments.py>`) Define a string that will be used as the comment template. There are available for that template the variables: 'label\_name', 'comment\_name', 'label\_time', 'comment\_time', 'label\_text' and 'comment\_text'. To use this just insert python standard substitutions: %(`<var name>`)s |
| comment\_only\_logged | (Default: False) If true only logged users can post comments |
| comment\_follow\_acl  | (Default: False) If true the user must have write permissions on the page to post comments  |
| comment\_subscribed\_notify | (Default: False) If true the users that subscribe the page where the comment was posted will be notified |
| comment\_passpartout\_group | (Default: PasspartoutGroup) MoinMoin user group. The users defined on this group will not be moderated or have captchas shown. |
| comment\_approval\_page       | (Default: CommentsApproval) This is the page name where the moderation queue is shown. Please note that the 'ApproveComments' macro must be present somewhere on this page. Also, this page is not auto-created, you have to create it at set the appropriate ACLs on it. |
| comment\_store\_addr | (Default: False) If enabled the commenter IP address will be saved in the comment file. |
| comment\_cmt\_per\_page | (Default: 50) Number of comments to show per page. After this number pagination controls will be shown. |
| comment\_recaptcha | (Default: False) If enabled the user will have to fill out a captcha (of the reCAPTCHA variety). Naturally if you want to use a reCAPTCHA you must also provide the following configuration options. |
| comment\_recaptcha\_public\_key | (Default: None) String with the reCAPTCHA public key |
| comment\_recaptcha\_private\_key | (Default: None) String with the reCAPTCHA private key |

This options should be defined on the wiki configuration file. None of this options is mandatory.
