import json
from pathlib import Path

from fastapi import APIRouter

from shared.logger import setup_logger
from shared.schemas import Item

logger = setup_logger("items")
router = APIRouter(prefix="/items", tags=["Items"])


@router.get("")
async def get_items():
    with open(Path(__file__).parent.parent / "items.json", "r") as f:
        raw = json.load(f)

    return [Item(**item) for item in raw]
