'''BlockExtend, extend template using another base template.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
from .exceptions import DefineBlockError
from .constants import (
    LINE_BLOCK,
    LINE_MACRO,
    LINE_COMMENT,
    LINE_INCLUDE,
    LINE_END,
    FILENAME)


class BlockExtend:

    RE_EXTEND = re.compile(r'^\s*#extend\s+([{FILENAME}]+)\s*:\s*$'
                           .format(FILENAME=FILENAME),
                           re.UNICODE)

    def __init__(self, lines):
        '''Initialize #extend.

        Note: extends 'lines' with content of the given filename.
        '''
        from .block import Block
        fn = self._compile(lines)
        self._block = Block(lines,
                            allowed=LINE_BLOCK |
                            LINE_MACRO |
                            LINE_COMMENT |
                            LINE_INCLUDE |
                            LINE_END)
        lines.extend(fn)

    def render(self, namespace):
        return self._block.render(namespace)

    @classmethod
    def _compile(cls, lines):
        '''Return the filename from the current line.'''
        m = cls.RE_EXTEND.match(lines.current)
        if m is None:
            raise DefineBlockError('''Incorrect block definition at line {}, {}
Should be something like: #extend path/foo.html:'''.format(
                lines.pos, lines.current))
        return m.group(1)
