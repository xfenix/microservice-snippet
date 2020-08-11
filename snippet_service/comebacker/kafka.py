"""Kafka comebacker."""
import asyncio
import logging

import orjson
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError

from snippet_service import settings


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


async def kafka_comebacker(meta_data: dict) -> None:
    """Very simple kafka sender."""
    producer_obj: AIOKafkaProducer = AIOKafkaProducer(
        loop=asyncio.get_event_loop(),
        bootstrap_servers=settings.KAFKA_COMEBACKER_BOOTSTRAP,
        value_serializer=lambda value: orjson.dumps(value).encode(),
    )
    await producer_obj.start()
    try:
        await producer_obj.send_and_wait(settings.KAFKA_COMEBACKER_TOPIC, meta_data)
    except KafkaError:
        LOGGER_OBJ.exception("Exception happens during kafka comeback")
    finally:
        await producer_obj.stop()
