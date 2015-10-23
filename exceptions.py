class TRenderException(Exception):
    pass


class CompileException(TRenderException):
    pass


class RenderException(TRenderException):
    pass


class UnexpectedBlockError(CompileException):
    pass


class DefineBlockError(CompileException):
    pass


class MacroBlockUsageError(CompileException):
    pass


class MissingInNamespaceError(RenderException):
    pass


class EvaluateError(RenderException):
    pass


class MacroOrBlockExistError(RenderException):
    pass


class MacroOrBlockNotDefinedError(RenderException):
    pass