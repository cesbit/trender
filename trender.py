import re
from lines import Lines
from block import Block
from namespace import Namespace
from constants import ALWAYS_ALLOWED, EOF_TEXT


class TRender:

    def __init__(self, text):
        lines = Lines(text.splitlines())
        self._block = Block(lines, allowed=ALWAYS_ALLOWED | EOF_TEXT)

    def render(self, namespace={}):
        if not isinstance(namespace, Namespace):
            namespace = Namespace(namespace)
        return self._block.render(namespace)


if __name__ == '__main__':
    import gc
    import time
    import sys
    # make sure we start empty
    gc.collect()

    template = TRender('''
<html>
Naam: @foo
#macro TEST:
    <itm>@item</itm>
#end
#block TEST_BLOCK:
    <block>@item</block>
#end
#if @debug:
<strong>hoi!</strong>
#else
<strong>dag!</strong>
#end
#TEST
#for @item in @items:
    <span>@item</span>
    #TEST
    #TEST_BLOCK
#end
<span>Einde!</span>
</html>
''')
    start = time.time()
    result = template.render({
        'foo': 'Iriske!',
        'debug': False,
        'items': ['Iris', 'Sasientje', 'Joente']
    })
    t = time.time() - start
    print(result, '\n\nRendered in {}, Collected items: {}'.format(t, gc.collect()))


