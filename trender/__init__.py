'''TRender - Python template parser.

Changelog

Version 1.0.7
    - Fixed correct version number

Version 1.0.6
    - Fixed bug in aiohttp template decorator (see github issue #2)

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
__email__ = 'jeroen@transceptor.technology'
__version__ = '1.0.7'
