'''TRender (Template Render Engine)

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

from .lines import Lines
from .block import Block
from .namespace import Namespace
from .constants import ALWAYS_ALLOWED, EOF_TEXT


class TRender:

    def __init__(self, content_or_file, path=None):
        lines = Lines(content_or_file, path)
        self._block = Block(lines, allowed=ALWAYS_ALLOWED | EOF_TEXT)

    def render(self, namespace={}):
        if not isinstance(namespace, Namespace):
            namespace = Namespace(namespace)
        return self._block.render(namespace)
