'''BlockPaste, use a macro or block.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
from .exceptions import MacroBlockUsageError
from .constants import VAR


class BlockPaste:

    RE_PASTE = re.compile(r'^\s*#([{VAR}]+)\s*$'.format(VAR=VAR), re.UNICODE)

    def __init__(self, lines):
        '''Initialize a paste #block or #macro.'''
        self._name = self._compile(lines)

    def render(self, namespace):
        '''Render a macro or block.

        Note: a macro is actually already rendered and will just return its
              rendered content.
        '''
        return namespace.get_macro_or_block(self._name)

    @classmethod
    def _compile(cls, lines):
        '''Return macro or block name from the current line.'''
        m = cls.RE_PASTE.match(lines.current)
        if m is None:
            raise MacroBlockUsageError(
                'Incorrect macro or block usage at line {}, {}\nShould be '
                'something like: #my_macro'.format(lines.pos, lines.current))
        return m.group(1)
