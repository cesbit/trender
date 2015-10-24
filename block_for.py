import re
from .exceptions import DefineBlockError
from .constants import ALWAYS_ALLOWED, LINE_END


class BlockFor:

    RE_FOR = re.compile('^\s*#for\s+@([a-zA-Z_]+)\s+in\s+@([a-zA-Z_]+)\s*:\s*$', re.UNICODE)

    def __init__(self, lines):
        from .block import Block
        self._item, self._items = self._compile(lines)
        self._block = Block(lines, allowed=ALWAYS_ALLOWED | LINE_END)

    def render(self, namespace):
        ns = namespace.copy()
        result = []
        for item in namespace[self._items]:
            ns[self._item] = item
            result.append(self._block.render(ns))
        return '\n'.join(result) if result else None

    def _compile(self, lines):
        m = self.RE_FOR.match(lines.current)
        if m is None:
            raise DefineBlockError('Incorrect block definition at line {}, {}\nShould be something like: #for @item in @items:'.format(lines.pos, lines.current))
        return m.group(1), m.group(2)
