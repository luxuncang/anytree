# -*- coding: utf-8 -*-


class Walker(object):

    def __init__(self):
        """Walk from one node to another."""
        super(Walker, self).__init__()

    def walk(self, start, end):
        """
        Walk from `start` node to `end` node.

        Returns:
            (upwards, downwards): `upwards` is a list of edges to parent nodes to go upward to.
            `downwards` is a list of edges to child nodes to go downward to.

        Raises:
            WalkError: on no common root node.

        >>> from anytree import Node, RenderTree, AsciiStyle
        >>> f = Node("f")
        >>> b = Node("b", parent=f)
        >>> a = Node("a", parent=b)
        >>> d = Node("d", parent=b)
        >>> c = Node("c", parent=d)
        >>> e = Node("e", parent=d)
        >>> g = Node("g", parent=f)
        >>> i = Node("i", parent=g)
        >>> h = Node("h", parent=i)
        >>> print(RenderTree(f, style=AsciiStyle()))
        Node('/f')
        |-- Node('/f/b')
        |   |-- Node('/f/b/a')
        |   +-- Node('/f/b/d')
        |       |-- Node('/f/b/d/c')
        |       +-- Node('/f/b/d/e')
        +-- Node('/f/g')
            +-- Node('/f/g/i')
                +-- Node('/f/g/i/h')

        Create a walker:

        >>> w = Walker()

        This class is made for walking:

        >>> w.walk(f, f)
        ([], [])
        >>> w.walk(f, b)
        ([], [Node('/f/b')])
        >>> w.walk(b, f)
        ([Node('/f')], [])
        >>> w.walk(a, f)
        ([Node('/f/b'), Node('/f')], [])
        >>> w.walk(b, f)
        ([Node('/f')], [])
        >>> w.walk(h, e)
        ([Node('/f/g/i'), Node('/f/g'), Node('/f')], [Node('/f/b'), Node('/f/b/d'), Node('/f/b/d/e')])

        For a proper walking the nodes need to be part of the same tree:

        >>> w.walk(Node("a"), Node("b"))
        Traceback (most recent call last):
          ...
        anytree.walker.WalkError: Node('/a') and Node('/b') are not part of the same tree.
        """
        s = start.path
        e = end.path
        if start.root != end.root:
            msg = "%r and %r are not part of the same tree." % (start, end)
            raise WalkError(msg)
        # common
        c = tuple([si for si, ei in zip(s, e) if si is ei])
        assert c[0] is start.root
        cs = len(c) - 1
        # up
        if start is c[-1]:
            up = []
        else:
            up = list(reversed(s[cs:-1]))
        # down
        if end is c[-1]:
            down = []
        else:
            down = list(e[cs + 1:])
        return up, down


class WalkError(RuntimeError):

    """Walk Error."""
