# Installation

First checkout the latest version from the repository:

    $ git clone https://github.com/heldergg/moin-comments.git

Next you have to copy the macros to the appropriate directory. Find out what's
your `data_dir` and:

    $ cp moin-comments/macro/* <data_dir>/plugin/macro/

Under the `moin-comments-read-only/optional` you have a cascading style sheet
that you may use with moin-comments. If you choose to do so you must copy it to
a web accessible place and make it available on the pages that have comments,
and comment forms. If you are planning to have comments on most pages you can
just include it in the global CSS.

## Configuration

You may define on your wiki configuration the following options (default
values shown):

    comment_moderate = True
    comment_approval_page = 'CommentsApproval'
    comment_store_addr = False
    comment_cmt_per_page = 50

    comment_recaptcha = False
    comment_recaptcha_public_key = None
    comment_recaptcha_private_key = None
    comment_recaptcha_use_ssl = False

To have reCAPTCHA support the reCAPTCHA client library (for python) is needed.
Right now I'm upgrading the code to use reCaptcha V2. Stay tunned.

