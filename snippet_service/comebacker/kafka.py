"""Kafka comebacker."""
import asyncio

import orjson
from aiokafka import AIOKafkaProducer

from snippet_service import exceptions, settings


async def kafka_comebacker(meta_data: dict) -> None:
    """Very simple kafka sender."""
    producer_obj: AIOKafkaProducer = AIOKafkaProducer(
        loop=asyncio.get_event_loop(),
        bootstrap_servers=settings.KAFKA_COMEBACKER_DESTINATON,
        value_serializer=lambda value: orjson.dumps(value).encode(),
    )
    await producer_obj.start()
    try:
        await producer_obj.send_and_wait(settings.KAFKA_COMEBACKER_TOPIC, meta_data)
    finally:
        await producer_obj.stop()
