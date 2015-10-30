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

    RE_EXTEND = re.compile('^\s*#extend\s+([{FILENAME}]+)\s*:\s*$'.format(FILENAME=FILENAME), re.UNICODE)

    def __init__(self, lines):
        from .block import Block
        fn = self._compile(lines)
        self._block = Block(lines, allowed=LINE_BLOCK | LINE_MACRO | LINE_COMMENT | LINE_INCLUDE | LINE_END)
        lines.extend(fn)

    def render(self, namespace):
        return self._block.render(namespace)

    def _compile(self, lines):
        m = self.RE_EXTEND.match(lines.current)
        if m is None:
            raise DefineBlockError('''Incorrect block definition at line {}, {}
Should be something like: #extend path/foo.html:'''.format(lines.pos, lines.current))
        return m.group(1)
