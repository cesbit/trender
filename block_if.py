import re
from exceptions import DefineBlockError
from exceptions import MissingInNamespaceError
from constants import (
    ALWAYS_ALLOWED,
    LINE_ELIF,
    LINE_ELSE,
    LINE_END)


class BlockIf:

    RE_IF = re.compile('^\s*#(if|elif)\s+@([a-zA-Z_]+)\s*:\s*$', re.UNICODE)

    def __init__(self, lines):
        from block import Block
        m = self.RE_IF.match(lines.current)
        if m is None:
            raise DefineBlockError('Incorrect block definition at line {}, {}\nShould be something like: #if @foo:'.format(line.pos, line.current))

        self._evaluate = m.group(2)

        self._block_true = Block(lines, allowed=ALWAYS_ALLOWED | LINE_ELIF | LINE_ELSE | LINE_END)
        self._block_false = Block(lines, allowed=ALWAYS_ALLOWED | LINE_END) if lines.current_type == LINE_ELSE else None

    def render(self, namespace):
        if self._evaluate not in namespace:
            raise MissingInNamespaceError('Missing in namespace: {}'.format(self._evaluate))
        if namespace[self._evaluate]:
            return self._block_true.render(namespace)
        if self._block_false is not None:
            return self._block_false.render(namespace)
        return ''



