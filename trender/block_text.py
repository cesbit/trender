'''BlockText, used to parse text with variable etc.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
from .constants import VAR_DOTS


class BlockText:

    RE_VAR = re.compile('@([{VAR_DOTS}]+)(!?)'.format(VAR_DOTS=VAR_DOTS),
                        re.UNICODE)

    def __init__(self, text):
        '''Initialize template line (or lines).'''
        self._need_format = False
        self._text = self._compile(text)

    def render(self, namespace):
        '''Render template lines.

        Note: we only need to parse the namespace if we used variables in
              this part of the template.
        '''
        return self._text.format_map(namespace.dictionary) \
            if self._need_format else self._text

    def _compile(self, text):
        # replace curly braces wit double curly so the will be
        # escaped when using format.
        text = text.replace('{', '{{').replace('}', '}}')

        # when variable are found we will also set _need_format to True
        text = self.__class__.RE_VAR.sub(self._set_vars, text)

        # replace escaped @! characters with just @
        text = text.replace('@!', '@')

        # undo the escaping when formatting is not needed
        if not self._need_format:
            text = text.replace('{{', '{').replace('}}', '}')
        return text

    def _set_vars(self, m):
        '''Set _need_format to True and return the variable wrapped in curly
        braces so it can be formatted.'''
        self._need_format = True
        return '{' + m.group(1).replace('.', '-') + '}'
