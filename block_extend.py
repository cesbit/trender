import re
from .exceptions import DefineBlockError
from .constants import (
    LINE_BLOCK,
    LINE_MACRO,
    FILENAME)


class BlockExtend:

    RE_EXTEND = re.compile('^\s*#extend\s+([{FILENAME}]+)\s*$'.format(FILENAME=FILENAME), re.UNICODE)

    def __init__(self, lines):
        from .block import Block
        self._evaluate = self._compile(lines)
        self._block_true = Block(lines, allowed= | LINE_END)
        if lines.current_type == LINE_ELSE:
            self._block_false = Block(lines, allowed=ALWAYS_ALLOWED | LINE_END)
        elif lines.current_type == LINE_ELIF:
            self._block_false = BlockIf(lines)
        else:
            self._block_false = None

    def render(self, namespace):
        if namespace[self._evaluate]:
            return self._block_true.render(namespace)
        if self._block_false is not None:
            return self._block_false.render(namespace)
        return None

    def _compile(self, lines):
        m = self.RE_IF.match(lines.current)
        if m is None:
            raise DefineBlockError('Incorrect block definition at line {}, {}\nShould be something like: #if @foo:'.format(lines.pos, lines.current))
        return m.group(2).replace('.', '-')
