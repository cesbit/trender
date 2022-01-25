'''BlockFor, create a for loop.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
from .exceptions import DefineBlockError
from .constants import (
    ALWAYS_ALLOWED,
    LINE_END,
    VAR,
    VAR_DOTS
)


class BlockFor:

    RE_FOR = re.compile(
        r'^\s*#for\s+@([{VAR}]+)\s+in\s+@([{VAR_DOTS}]+)\s*:\s*$'
        .format(VAR=VAR, VAR_DOTS=VAR_DOTS),
        re.UNICODE)

    def __init__(self, lines):
        '''Initialize #for.'''
        from .block import Block
        self._item, self._items = self._compile(lines)
        self._block = Block(lines, allowed=ALWAYS_ALLOWED | LINE_END)

    def render(self, namespace):
        '''Render #for loop with given namespace.

        Note: we copy the namespace so the parsed variable is only
              available in nested objects within this #for loop.
        '''
        ns = namespace.copy()
        result = []
        for item in namespace[self._items]:
            ns[self._item] = item
            result.append(self._block.render(ns))
        return '\n'.join(result) if result else None

    @classmethod
    def _compile(cls, lines):
        '''Return both variable names used in the #for loop in the
        current line.'''
        m = cls.RE_FOR.match(lines.current)
        if m is None:
            raise DefineBlockError(
                'Incorrect block definition at line {}, {}\nShould be '
                'something like: #for @item in @items:'
                .format(lines.pos, lines.current))
        return m.group(1), m.group(2).replace('.', '-')
