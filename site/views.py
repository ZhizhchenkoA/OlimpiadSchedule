from aiohttp import web
from aiohttp_jinja2 import render_template_async as render_template
from aiohttp.web import BaseRequest

routes = web.RouteTableDef()


@routes.get('/')
async def index_handler(request: BaseRequest):
    return await render_template(template_name='index.html', request=request, context={})


@routes.get('/add_olimpiad')
async def add_olimpiad(request: BaseRequest):
    return await render_template(template_name='add_olimpiad.html', request=request, context={})


@routes.post('/add_stages')
async def add_stages(request: BaseRequest):
    data = await request.post()
    print(**data)
    return
