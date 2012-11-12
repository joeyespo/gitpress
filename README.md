Gitpress
========

Beautiful blogging for hackers.

Gitpress transforms this

    /
    +- 2011/
    |    +- 01-init.md
    +- 2012/
    |    +- 01-welcome-to-gitpress.md
    |    +- 02-tips-for-gitpress.md
    +- README.md

into a living, breathing website.

Gitpress takes full advantage of Git. There's no roles, timestamps, or authors
mixed with the content by default. This metadata is inferred.

You can customize the layout and theme with an independent **presentation**
repository, effectively separating your content and presentation concerns.


Why?
----

How many times have you put off writing because you couldn't settle on a CMS?
Or wanted to switch services, but felt overwhelmed by the amount of work
involved? Have you ever been inspired to write but then wasted it on *setting
up* the blog?

Gitpress is here to help.

#### For new blogs ####

Write first. Publish for review. Iterate your story based on real feedback.
**All before you deploy**. As a bonus, it's much easier to customize
the style of your site when you have some content to work with.

#### For collaboration ####

With the power of a distributed version control system, you can host your
content like any other project and allow your words to evolve socially. Pull
in corrections, site improvements, or even outsource or fork a front-end
completely as you write, without bottleneck.

#### For the future ####

Gitpress was created with the belief that your content and your presentation
shouldn't mingle. By decoupling these layers, you're no longer locked into a
single host or even a particular blogging platform. You can focus on
what's most important from day one. Your *writing*.


Getting Started: Writers
------------------------

Youl'll begin like you would any other programming project.

1. `mkdir myblog`
2. `cd myblog`
3. `git init`

Then create your `README.md` to indicate this is your blog content.


File Conventions
----------------

File organization is extremely flexible. The rules are:

1. Files and directories beginning with a letter are **named**
3. Files and directories containing numbers without letters are **indexed**
2. Files and directories beginning with a number,
   containing letters are **ordered named**

The special characters `!@#$%^&()_-+=,.[]{}'` are allowed and are ignored by the above.
The rules are sensible for blogging and are used in the lookup process
described in the next section.

For example:

    /
    +- 2012
    |    + 01-first.md
    |    + 02-second.md
    + index.md     
    + README.md

Frequent writers may prefer:

    /
    +- 2012
    |    +- 10
    |    |   + 01-my-first-post.md
    |    |   + 02-another-in-october.md
    |    +- 11
    |        + 01-movember-has-arrived.md
    |        + 02-how-to-grow-a-moustache.md
    + index.md     
    + README.md

Both of these examples can re-use the same front-end.
