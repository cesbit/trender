import re
from .exceptions import DefineBlockError
from .constants import ALWAYS_ALLOWED, LINE_END


class BlockMacro:

    RE_MACRO = re.compile('^\s*#macro\s+([a-zA-Z_]+)\s*:\s*$', re.UNICODE)

    def __init__(self, lines):
        from .block import Block
        self._name = self._compile(lines)
        self._block = Block(lines, allowed=ALWAYS_ALLOWED | LINE_END)

    def render(self, namespace):
        namespace.add_macro(self._name, self._block)
        return None

    def _compile(self, lines):
        m = self.RE_MACRO.match(lines.current)
        if m is None:
            raise DefineBlockError('Incorrect macro definition at line {}, {}\nShould be something like: #macro my_macro:'.format(lines.pos, lines.current))
        return m.group(1)
