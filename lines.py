import re
from .constants import MAP_LINE_TYPE, LINE_PASTE


class Lines:

    RE_BLOCK = re.compile('\s*#([a-zA-Z_]*)', re.UNICODE)

    def __init__(self, lines):
        self._lines = lines
        self._gen_lines = self._reader()

    @property
    def next(self):
        try:
            line = next(self._gen_lines)
            self.current_type = self._get_current_type(line)
            return line

        except StopIteration:
            return None

    def _reader(self):
        for self.pos, line in enumerate(self._lines):
            yield line

    def __len__(self):
        return len(self._lines)

    @property
    def current(self):
        return self._lines[self.pos]

    @classmethod
    def _get_current_type(cls, line):
        m = cls.RE_BLOCK.match(line)
        return MAP_LINE_TYPE.get(m.group(1) if m else None, LINE_PASTE)
