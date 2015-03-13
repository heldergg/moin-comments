#summary Moin-Comments installtion
#labels Featured

# Installation #

If you're using MoinMoin 1.9.x do a checkout of the latest version from the repository:

```
$ svn checkout http://moin-comments.googlecode.com/svn/trunk/ moin-comments-read-only
```

If you're using MoinMoin 1.8.x you'll have to checkout [revision 39](https://code.google.com/p/moin-comments/source/detail?r=39) from the repo (you should really upgrade to the latest MoinMoin release however).

Next you have to copy the macros to the appropriate directory. Find out what's your ''data\_dir'' and:

```
$ cp moin-comments-read-only/macro/* <data_dir>/plugin/macro/
```

Under the ''`moin-comments-read-only/optional`'' you have a cascading style sheet that you may use with moin-comments. If you choose to do so you must copy it to a web accessible place and make it available on the pages that have comments, and comment forms. If you are planning to have comments on most pages you can just include it in the general CSS.

By default the comments are moderated, you can set the comment\_moderate to false if you do not want moderated comments (if for instance you're using a captcha). If you want moderated comments you'll have to create the page `CommentsApproval`, the comments will be stored there until approval or deletion. You'll need also to add anywhere in this page the macro `ApproveComments`.

To have reCAPTCHA support the reCAPTCHA client library (for python) is needed,
you can get it from:

  * http://code.google.com/p/recaptcha
  * http://code.google.com/p/recaptcha/source/browse/trunk/recaptcha-plugins/python/recaptcha/client/captcha.py

Naturally you must also be registed in recaptcha.net to get a pair of
public/private keys for the reCAPTCHA API. Once you have the keys you must use the configuration options bellow to enable the reCAPTCHA support.

# Configuration #

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
| comment\_recaptcha\_use\_ssl | (Default: False) Make the reCAPTCHA requests using ssl |

This options should be defined on the wiki configuration file. None of this options is mandatory.