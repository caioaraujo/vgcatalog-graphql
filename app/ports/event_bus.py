from abc import ABC, abstractmethod

class EventBus(ABC):

    @abstractmethod
    def publish(self, event_type: str, payload: dict) -> None:
        pass
