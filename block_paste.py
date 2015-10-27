import re
from .exceptions import MacroBlockUsageError
from .constants import VAR


class BlockPaste:

    RE_PASTE = re.compile('^\s*#([{VAR}]+)\s*$'.format(VAR=VAR), re.UNICODE)

    def __init__(self, lines):
        self._name = self._compile(lines)

    def render(self, namespace):
        return namespace.get_macro_or_block(self._name)

    def _compile(self, lines):
        m = self.RE_PASTE.match(lines.current)
        if m is None:
            raise MacroBlockUsageError('Incorrect macro or block usage at line {}, {}\nShould be something like: #my_macro'.format(lines.pos, lines.current))
        return m.group(1)
