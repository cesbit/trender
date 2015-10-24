from .block_text import BlockText
from .block_if import BlockIf
from .block_for import BlockFor
from .block_macro import BlockMacro
from .block_block import BlockBlock
from .block_paste import BlockPaste
from .exceptions import UnexpectedBlockError
from .exceptions import UnexpectedEOFError
from .constants import (
    LINE_IF,
    LINE_ELIF,
    LINE_FOR,
    LINE_MARCO,
    LINE_BLOCK,
    LINE_ELSE,
    LINE_TEXT,
    LINE_END,
    LINE_PASTE,
    LINE_COMMENT,
    EOF_TEXT
)


class Block:

    def __init__(self, lines, allowed):
        self._blocks = []
        self._compile(lines, allowed)

    def render(self, namespace):
        return '\n'.join([text for text in [block.render(namespace) for block in self._blocks] if text is not None])

    def _compile(self, lines, allowed):
        self._text = []
        while lines.next is not None:
            if not allowed & lines.current_type:
                raise UnexpectedBlockError('Unexpected block at: {}, {}'.format(lines.pos, lines.current))

            if lines.current_type == LINE_COMMENT:
                continue

            if lines.current_type == LINE_IF or lines.current_type == LINE_ELIF:
                self._reset_plain()
                self._blocks.append(BlockIf(lines))
                continue

            if lines.current_type == LINE_FOR:
                self._reset_plain()
                self._blocks.append(BlockFor(lines))
                continue

            if lines.current_type == LINE_MARCO:
                self._reset_plain()
                self._blocks.append(BlockMacro(lines))
                continue

            if lines.current_type == LINE_BLOCK:
                self._reset_plain()
                self._blocks.append(BlockBlock(lines))
                continue

            if lines.current_type == LINE_PASTE:
                self._reset_plain()
                self._blocks.append(BlockPaste(lines))
                continue

            if lines.current_type == LINE_END or lines.current_type == LINE_ELSE:
                break

            if lines.current_type == LINE_TEXT:
                self._text.append(lines.current)
                continue

            raise RuntimeError('Damm, we should not get here. Current line:', lines.current)
        else:
            if not allowed & EOF_TEXT:
                raise UnexpectedEOFError('Unexpected end of file, missing #end')
        self._reset_plain()

    def _reset_plain(self):
        if self._text:
            self._blocks.append(BlockText('\n'.join(self._text)))
        self._text.clear()
