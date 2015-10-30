class TRenderException(Exception):
    pass


class CompileException(TRenderException):
    pass


class RenderException(TRenderException):
    pass


class UnexpectedBlockError(CompileException):
    pass


class UnexpectedEOFError(CompileException):
    pass


class DefineBlockError(CompileException):
    pass


class TemplateNotExistsError(CompileException):
    pass


class MacroBlockUsageError(CompileException):
    pass


class EvaluateError(RenderException):
    pass


class MacroOrBlockExistError(RenderException):
    pass


class MacroOrBlockNotDefinedError(RenderException):
    pass
