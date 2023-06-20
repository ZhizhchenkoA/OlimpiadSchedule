from aiohttp import web
from aiohttp_jinja2 import render_template
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index_handler(request):
    return
