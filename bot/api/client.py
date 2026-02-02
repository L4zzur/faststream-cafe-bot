import aiohttp

from shared.config import settings
from shared.logger import setup_logger
from shared.schemas import Item, OrderCreate, OrderCreated

logger = setup_logger("bot.api")


async def get_menu() -> list[Item]:
    url = settings.cashier_api_url + "api/items"
    logger.info(f"Sending menu request to {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                text = await response.text()
                logger.error(f"Failed to get menu: {text}")
                raise Exception(f"Order Service returned {response.status}: {text}")

            data = await response.json()
            return [Item.model_validate(item) for item in data]


async def create_order(order: OrderCreate) -> OrderCreated:
    url = settings.cashier_api_url + "api/order"
    logger.info(f"Sending order request to {url}: {order}")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=order.model_dump()) as response:
            logger.info(f"Order Service response: {response.status}")

            if response.status != 200:
                text = await response.text()
                logger.error(f"Failed to create order: {text}")
                raise Exception(f"Order Service returned {response.status}: {text}")

            data = await response.json()
            return OrderCreated.model_validate(data["data"])
