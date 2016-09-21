'''Use TRender with aiohttp.

This implementation is based on aiohttp_jinja2, see:
http://aiohttp-jinja2.readthedocs.org/en/stable/ and
https://github.com/aio-libs/aiohttp_jinja2

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''

from aiohttp import web
from .trender import TRender

_templates = {}


def template(template_name):
    # register this template name
    _templates[template_name] = None

    def wrapper(func):

        async def wrapped(*args):
            namespace = await func(*args)
            text = _templates[template_name].render(namespace)
            return web.Response(body=text.encode('utf-8'))
        return wrapped
    return wrapper


def setup_template_loader(template_path):
    for template_name in _templates:
        _templates[template_name] = TRender(template_name, path=template_path)
