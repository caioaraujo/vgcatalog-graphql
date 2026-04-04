import json

from confluent_kafka import Producer

from app.domain.events.event_bus import EventBus


class KafkaEventBus(EventBus):
    def __init__(self, bootstrap_server: str) -> None:
        self._producer = Producer(
            {
                "bootstrap.servers": bootstrap_server,
            }
        )

    def publish(self, event_type: str, payload: dict) -> None:
        self._producer.produce(
            topic=event_type,
            value=json.dumps(payload),
            callback=self._delivery_report,
        )

        self._producer.poll(0)

    def _delivery_report(self, err, msg) -> None:
        if err is not None:
            # TODO: Add logger
            print(f"[ERROR] Delivery failed: {err}")
        else:
            print(
                f"[INFO] Delivery succeeded to topic: {msg.topic()} [{msg.partition()}]"
            )
