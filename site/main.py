from aiohttp import web
from views import routes
import aiohttp_jinja2
import jinja2


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates/'),
                         enable_async=True)
    app.router.add_static('/static/', path='static/', name='static')
    web.run_app(app, host='0.0.0.0', port=8080)
