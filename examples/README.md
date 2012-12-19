Gitpress Examples
=================

Each subdirectory here contains an example **server project** that uses the
Gitpress API.

Note that these are examples of advanced uses. Most projects can simply:

```bash
$ gitpress serve <content-url> [<theme-url>]
```

#### Were you looking for example blogs?

They're in the branches of this repository. Try:

```bash
$ git checkout example-blog
```


Summary
-------

- [Simple][]: a minimal project that listens for Git pushes and serves them


More Examples
-------------

Take a look at the [blog server's source code][server] for a working
example and [the blog repository][content] for the content it presents.


[simple]: examples/simple/
[server]: https://github.com/joeyespo/gitpress-blog/tree/blog.gitpress.com
[content]: https://github.com/joeyespo/gitpress-blog
