import json

from confluent_kafka import Producer

from app.domain.events.event_bus import EventBus


class KafkaEventBus(EventBus):
    def __init__(self, producer: Producer) -> None:
        self._producer = producer

    def publish(self, event_type: str, payload: dict) -> None:
        self._producer.produce(topic=event_type, value=json.dumps(payload))
