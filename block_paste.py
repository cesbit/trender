import re
from exceptions import MacroBlockUsageError


class BlockPaste:

    RE_PASTE = re.compile('^\s*#([a-zA-Z_]+)\s*$', re.UNICODE)

    def __init__(self, lines):
        m = self.RE_PASTE.match(lines.current)
        if m is None:
            raise MacroBlockUsageError('Incorrect macro or block usage at line {}, {}\nShould be something like: #my_macro'.format(lines.pos, lines.current))
        self._name = m.group(1)

    def render(self, namespace):
        return namespace.get_macro_or_block(self._name)
