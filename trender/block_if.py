'''BlockIf, used for if, elif and else.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
from .exceptions import DefineBlockError
from .constants import (
    ALWAYS_ALLOWED,
    LINE_ELIF,
    LINE_ELSE,
    LINE_END,
    VAR_DOTS)


class BlockIf:

    RE_IF = re.compile(
        r'^\s*#(if|elif)\s+@([{VAR_DOTS}]+)(\s*\(\s*(@[{VAR_DOTS}]+\s*(,\s*'
        r'@[{VAR_DOTS}]+\s*)*)?\))?\s*:\s*$'
        .format(VAR_DOTS=VAR_DOTS),
        re.UNICODE)

    def __init__(self, lines):
        '''Initialize #if.

        Note: we both read the 'true' block and 'false' block and set the
              appropriate render method to use a boolean or a function
              as if-statement.
        '''
        from .block import Block
        self._compile(lines)
        self._block_true = Block(lines,
                                 allowed=ALWAYS_ALLOWED |
                                 LINE_ELIF |
                                 LINE_ELSE |
                                 LINE_END)
        if lines.current_type == LINE_ELSE:
            self._block_false = Block(lines,
                                      allowed=ALWAYS_ALLOWED |
                                      LINE_END)
        elif lines.current_type == LINE_ELIF:
            self._block_false = BlockIf(lines)
        else:
            self._block_false = None

    def render(self, namespace):
        '''Render a 'true' or (if available) 'false' block based on a
        boolean.'''
        if (self._isbool and
            namespace[self._evaluate]) or \
            (not self._isbool and
             namespace[self._evaluate](*[namespace[arg]
                                         for arg in self._args])):
            return self._block_true.render(namespace)
        if self._block_false is not None:
            return self._block_false.render(namespace)
        return None

    def _compile(self, lines):
        '''Set the correct render method (boolean or function call)
        and read variables from the current line.
        '''
        m = self.__class__.RE_IF.match(lines.current)
        if m is None:
            raise DefineBlockError(
                'Incorrect block definition at line {}, {}\nShould be '
                'something like: #if @foo:'.format(lines.pos, lines.current))
        args = m.group(3)
        self._evaluate = m.group(2).replace('.', '-')
        self._isbool = args is None
        if not self._isbool:
            args = args.strip('() \t')
            self._args = [arg.strip('@ \t').replace('.', '-')
                          for arg in args.split(',')]
