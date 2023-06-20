from aiohttp import web
from routes import setup_routes
import aiohttp_jinja2
import jinja2

app = web.Application()
setup_routes(app)
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('templates/'))
app.router.add_static('/static/', path='static/', name='static')
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
