from fastapi import FastAPI

import src.db as db
from src.routers import api_router
from src.exceptions.handlers import add_exception_handlers


def bind_events(app):
    @app.on_event('startup')
    async def startup():
        await db.open_db()

    @app.on_event('shutdown')
    async def shutdown():
        await db.close_db()


def get_app():
    app = FastAPI(title='lost&found')
    app.include_router(api_router, prefix='/api')
    bind_events(app)
    add_exception_handlers(app)
    return app


app = get_app()
