'''Use TRender with aiohttp.

This implementation is based on aiohttp_jinja2, see:
http://aiohttp-jinja2.readthedocs.org/en/stable/ and
https://github.com/aio-libs/aiohttp_jinja2

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''

from aiohttp import web
from .trender import TRender

_templates = {}

class _Template:
    def __init__(self, template_name, **kwargs):
        self.ctemplate = None
        self.kwargs = {
            'content_type': 'text/html',
            'charset': 'utf-8'
        }
        self.kwargs.update(kwargs)


def template(template_name, **kwargs):
    # register this template name
    rtemplate = _templates[template_name] = _Template(template_name, **kwargs)

    def wrapper(func):
        async def wrapped(*args):
            namespace = await func(*args)
            text = rtemplate.ctemplate.render(namespace)
            return web.Response(body=text.encode('utf-8'), **rtemplate.kwargs)

        return wrapped

    return wrapper


def setup_template_loader(template_path):
    for template_name in _templates:
        _templates[template_name].ctemplate = TRender(
            template_name,
            path=template_path)
