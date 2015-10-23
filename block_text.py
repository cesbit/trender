import re


class BlockText:

    RE_VAR = re.compile('@[a-zA-Z_]+', re.UNICODE)

    def __init__(self, text):
        self._text = self._compile(text)

    def render(self, namespace):
        return self._text.format_map(namespace.dictionary)

    def _compile(self, text):
        text = text.replace('{', '{{').replace('}', '}}')
        text = self.RE_VAR.sub(lambda m: '{' + m.group()[1:] + '}', text)
        text = text.replace('@!', '@')
        return text
