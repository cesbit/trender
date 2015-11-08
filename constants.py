LINE_IF = 1
LINE_ELSE = 2
LINE_ELIF = 4
LINE_END = 8
LINE_MACRO = 16
LINE_COMMENT = 32
LINE_BLOCK = 64
LINE_FOR = 128
LINE_PASTE = 256
LINE_TEXT = 512
LINE_INCLUDE = 1024
LINE_EXTEND = 2048
EOF_TEXT = 4096

ALWAYS_ALLOWED = (
    LINE_IF |
    LINE_MACRO |
    LINE_PASTE |
    LINE_TEXT |
    LINE_COMMENT |
    LINE_FOR |
    LINE_BLOCK |
    LINE_INCLUDE |
    LINE_EXTEND)

MAP_LINE_TYPE = {
    None: LINE_TEXT,
    'if': LINE_IF,
    'else': LINE_ELSE,
    'elif': LINE_ELIF,
    'end': LINE_END,
    'for': LINE_FOR,
    'macro': LINE_MACRO,
    'block': LINE_BLOCK,
    'include': LINE_INCLUDE,
    'extend': LINE_EXTEND,
    '': LINE_COMMENT
}

VAR = 'a-zA-Z0-9_'
VAR_DOTS = VAR + '\.'
FILENAME = 'a-zA-Z0-9_\./'
