'''Lines Class which is responsible for reading lines.

:copyright: 2015, Jeroen van der Heijden (Cesbit)
'''

import re
import os
from .constants import MAP_LINE_TYPE, LINE_PASTE, FILENAME
from .exceptions import DefineBlockError, TemplateNotExistsError


class Lines:

    RE_BLOCK = re.compile(r'\s*#([a-zA-Z_]*)', re.UNICODE)
    RE_INCLUDE = re.compile(r'^\s*#include\s+([{FILENAME}]+)\s*$'
                            .format(FILENAME=FILENAME), re.UNICODE)

    def __init__(self, content_or_file, path=None):
        self._path = path
        self._lines = content_or_file.splitlines() \
            if path is None \
            else self._read_template(content_or_file)
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

    def _read_template(self, fn):
        if self._path is None:
            raise DefineBlockError('''Incorrect block definition at line {}, {}
include/extend statements only work when starting with a file and path,
not with string content'''.format(self.pos, self.current))

        fn = os.path.join(self._path, fn)
        if not os.path.exists(fn):
            raise TemplateNotExistsError(
                'Cannot find template file: {}'.format(fn))

        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.splitlines()

    def include(self):
        m = self.__class__.RE_INCLUDE.match(self.current)
        if m is None:
            raise DefineBlockError('''Incorrect block definition at line {}, {}
Should be something like: #include path/foo.html'''.format(
                    self.pos, self.current))

        self._lines = \
            self._read_template(m.group(1)) + self._lines[self.pos + 1:]
        self._gen_lines = self._reader()

    def extend(self, fn):
        self._lines = self._read_template(fn) + self._lines[self.pos + 1:]
        self._gen_lines = self._reader()

    def __len__(self):
        return len(self._lines)

    @property
    def current(self):
        return self._lines[self.pos]

    @classmethod
    def _get_current_type(cls, line):
        m = cls.RE_BLOCK.match(line)
        return MAP_LINE_TYPE.get(m.group(1)
                                 if m else (True
                                 if line.strip() else None), LINE_PASTE)
