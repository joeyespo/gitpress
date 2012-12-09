Simple
======

A [Gitpress][repo] example that runs a server and listens for pushes.


Usage
-----

To try it, simply clone the repo, install the requirements, and run the script:

```bash
$ git clone git@github.com:joeyespo/gitpress.git
$ cd gitpress/examples/simple
$ pip install -r requirements.txt
$ python simple.py
```

You can now push a blog repository to localhost with git.
For example, using your local copy of Gitpress:

    $ git push git://localhost/ example-blog:master

Now visit `http://localhost:5000` in your browser.


[repo]: https://github.com/joeyespo/gitpress
