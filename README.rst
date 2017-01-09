globcopy -- copy partial subtrees from a to b
=============================================

This is a tiny tool to copy partial subtrees from a source to a target
directory. Subtrees are expressed using the glob syntax supported by
`glob2 <https://github.com/miracle2k/python-glob2/`_, i.e. including
'*', '?', character classes and the recursive glob pattern '**'.

Usage::

  globcopy source destination pat1 [pat2 ...]
