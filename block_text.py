import re


class BlockText:

    RE_VAR = re.compile('@[a-zA-Z_]+', re.UNICODE)

    def __init__(self, text):
        self._text = self._compile(text)
        self._need_format = False

    def render(self, namespace):
        print('here', self._need_format)
        return self._text.format_map(namespace.dictionary) if self._need_format else self._text

    def _compile(self, text):
        text = text.replace('{', '{{').replace('}', '}}')
        text = self.RE_VAR.sub(self._set_vars, text)
        text = text.replace('@!', '@')
        return text

    def _set_vars(self, m):
        self._need_format = True
        return '{' + m.group()[1:] + '}'