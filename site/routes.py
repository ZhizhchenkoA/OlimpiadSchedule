from views import index_handler


def setup_routes(app):
    app.router.add_get('/', index_handler)
