from aiogram import Router


def setup_message_routers() -> Router:
    from . import menu, order, start

    router = Router()
    router.include_router(menu.router)
    router.include_router(start.router)
    router.include_router(order.router)
    return router
