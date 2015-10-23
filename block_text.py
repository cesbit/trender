import re


class BlockText:

    RE_VAR = re.compile('@[a-zA-Z_]+', re.UNICODE)

    def __init__(self, text):
        self._text = self._compile(text)

    def render(self, namespace):
        _temp = self._dict.copy()
        _temp.update(namespace.dictionary)
        return self._text.format(**_temp)

    def _compile(self, text):
        self._dict = {}
        text = text.replace('{', '{{').replace('}', '}}')
        text = self.RE_VAR.sub(self._build_required_dict, text)
        text = text.replace('@!', '@')
        return text

    def _build_required_dict(self, m):
        var = m.group()[1:]
        self._dict[var] = ''
        return '{' + var + '}'
