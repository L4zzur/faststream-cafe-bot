from fastapi import APIRouter

from . import item, order

router = APIRouter(prefix="/api")
router.include_router(item.router)
router.include_router(order.router)
