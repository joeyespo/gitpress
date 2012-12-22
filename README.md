Gitpress -- Blissful blogging for hackers
=========================================

Gitpress transforms this

    /
    +- 2011/
    |    +- 01-init.md
    +- 2012/
    |    +- 01-welcome-to-gitpress.md
    |    +- 02-tips-for-gitpress.md
    +- README.md

into a living, breathing website.


What?
-----

Gitpress is a collection of tools for working with presentation-less blog
repositories. Your layout and theme can be customized independently,
effectively separating your content and presentation concerns.

Gitpress also takes full advantage of git. There's no *roles*, *timestamps*, or
*authors* mixed in with your content by default. This metadata is all inferred.


Why?
----

How many times have you put off writing because you couldn't settle on a CMS?
Or wanted to switch services, but felt overwhelmed by the amount of work
involved? Have you ever been inspired to write but then wasted it on *setting
up* the blog? Gitpress is here to help.

#### For new blogs

Write first. Git-push for review and comments. Iterate your story based on real
feedback. **All before you publish**. As a bonus, it's much easier to customize
the style of your site when you have some content to work with.

#### For collaboration

With the power of a distributed version control system, you can host your
content like any other project and allow your words to evolve socially. Pull
in corrections, site improvements, or even outsource or fork a front-end
completely as you write, without bottleneck.

#### For the future

Gitpress was created with the belief that your content and your presentation
shouldn't mingle. By decoupling these layers, you're no longer locked into a
single host, particular blogging platform, or even how you organize your files.
Through any change, you can still keep your focus on what's most important
since day one. *Your writing*.


Getting Started: Writing
------------------------

You'll begin like you would any other programming project:

    $ mkdir myblog
    $ cd myblog
    $ git init

You should also create a `README.md` file if you're feeling generous,
indicating this repository contains the content of your blog.

Now you can begin writing. Create a new Markdown file for each blog post.
Commit normally. Push to publish. The only requirement is that you prefix
any files or directories that you want shown in a particular order with a
number. You may want a directory for each year:

    /
    +- 2012
        +- 01-my-first-post.md

That way you don't end up with too many files in one place as
your story unfolds.

#### File conventions

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
    |    +- 01-first.md
    |    +- 02-second.md
    +- README.md

Daily writers may prefer:

    /
    +- 2012
    |    +- 10
    |    |   +- 01-my-first-post.md
    |    |   +- 20-another-in-october.md
    |    +- 11
    |        +- 01-movember-has-arrived.md
    |        +- 11-growing-a-moustache.md
    |        +- 18-wheres-my-moustache.md
    |        +- 28-moustache-finally-arrived.md
    +- README.md

What's important is that *you* are comfortable with your files. There's no need
to get hung up over this. Start with something simple. Reorganize later, moving
your posts into month-based sub-directories. And you can do this without making
a mess of your permalinks, since that's all handled by your presentation layer.


Next Steps: Presenting
----------------------

Now that you have a simple repository containing some amazing content, it's
time to get your work out there. There's a few options.

#### Deploy with Git

Simply push your work to an existing Gitpress server:

    $ git push mysite

#### The command-line interface

Install Gitpress using [pip][]:

    $ pip install gitpress

You can preview your working directory without committing anything:

    $ gitpress preview
     * Running on http://localhost:5000/

This uses the default presentation configuration by default. Locate the admin
page from there to change the layout and theme.


Setting up a Gitpress Server
----------------------------

There's no command-line interface to fully serve a Gitpress website. Instead,
you'll need to create a small Python web script that imports Gitpress. This
allows server projects to include their own dependencies and optimizations.
You can also override the functionality of any of the components as needed.

### Push-based

*Note: this feature is [being designed](#4), planned for a future release.*

The simplest thing to do is let Gitpress listen for a push and handle the rest:

```python
import gitpress

if __name__ == '__main__':
    gitpress.run(port=8080)
```

Save the above to a file called `server.py` and run it:

```bash
$ python server.py
 * Running on http://localhost:8080/
```

To see your blog in action, Git-push to localhost. For example:

```bash
git clone git@github.com:joeyespo/gitpress-blog.git
cd gitpress
git push git://localhost/
```

### Pull-based

*Note: this feature is still [being developed](#3), planned for next release.*

Pull-based is similar to push-based, only you'll provide the repository to pull
from, guaranteeing it comes from the right place. You'll be able to trigger a
pull manually from the Admin interface or by setting up [post-receive hooks][].

```python
import gitpress

if __name__ == '__main__':
    gitpress.run('http://github.com/joeyespo/gitpress-blog.git')
```

Save the above to a file called `pull_server.py` and run it:

```bash
$ python pull_server.py
 * Running on http://localhost:5000/
```

Like the preview, you can further configure Gitpress by visiting the Admin page
of your blog with the browser. You can also configure Gitpress directly using
the API, or design it to consume its own command-line arguments. The next
section goes into more detail and demonstrates the flexibility of the API.


The Python API
--------------

*TODO*


[pip]: http://pypi.python.org/pypi/pip
[post-receive hooks]: https://help.github.com/articles/post-receive-hooks
