'''BlockMacro, define a macro.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
from .exceptions import DefineBlockError
from .constants import ALWAYS_ALLOWED, LINE_END


class BlockMacro:

    RE_MACRO = re.compile(r'^\s*#macro\s+([a-zA-Z0-9_]+)\s*:\s*$', re.UNICODE)

    def __init__(self, lines):
        '''Initialize #macro.'''
        from .block import Block
        self._name = self._compile(lines)
        self._block = Block(lines, allowed=ALWAYS_ALLOWED | LINE_END)

    def render(self, namespace):
        '''Add the macro to the namespace.

        Note: at this point the macro will be rendered.
        '''
        namespace.add_macro(self._name, self._block)
        return None

    @classmethod
    def _compile(cls, lines):
        '''Return the macro name from the current line.'''
        m = cls.RE_MACRO.match(lines.current)
        if m is None:
            raise DefineBlockError(
                'Incorrect macro definition at line {}, {}\nShould be '
                'something like: #macro my_macro:'
                .format(lines.pos, lines.current))
        return m.group(1)
