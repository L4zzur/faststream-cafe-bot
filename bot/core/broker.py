from faststream.rabbit import RabbitBroker

from shared.config import settings

broker = RabbitBroker(settings.rabbit_url)
