from .exceptions import MacroOrBlockExistError
from .exceptions import MacroOrBlockNotDefinedError


class Namespace:

    def __init__(self, dictionary=None, macros=None, blocks=None):
        self.dictionary = dictionary or {}
        self._macros = macros or {}
        self._blocks = blocks or {}

    def __iter__(self):
        return self.dictionary.__iter__()

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        self.dictionary[key] = value

    def keys(self):
        return self.dictionary.keys()

    def values(self):
        return self.dictionary.keys()

    def copy(self):
        return Namespace(self.dictionary.copy(), self._macros, self._blocks)

    def get_macro_or_block(self, name):
        if name in self._macros:
            return self._macros[name]
        if name in self._blocks:
            return self._blocks[name].render(self)
        raise MacroOrBlockNotDefinedError('macro or block {} is not defined'.format(name))

    def has_macro_or_block(self, name):
        return name in self._macros or name in self._blocks

    def add_macro(self, name, block):
        if self.has_macro_or_block(name):
            raise MacroOrBlockExistError('macro or block {} already defined'.format(name))
        self._macros[name] = block.render(self)

    def add_block(self, name, block):
        if self.has_macro_or_block(name):
            raise MacroOrBlockExistError('macro or block {} already defined'.format(name))
        self._blocks[name] = block
