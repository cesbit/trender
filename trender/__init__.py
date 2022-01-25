'''TRender - Python template parser.

:copyright: 2022, Jeroen van der Heijden (Cesbit)
:license: MIT
'''

from .trender import TRender
from .exceptions import (
    TRenderException,
    CompileException,
    RenderException,
    MacroOrBlockNotDefinedError,
    MacroOrBlockExistError,
    UnexpectedBlockError,
    UnexpectedEOFError,
    DefineBlockError,
    TemplateNotExistsError,
    MacroBlockUsageError)

__author__ = 'Jeroen van der Heijden'
__maintainer__ = 'Jeroen van der Heijden'
__email__ = 'jeroen@cesbit.com'
__version__ = '1.0.8'
