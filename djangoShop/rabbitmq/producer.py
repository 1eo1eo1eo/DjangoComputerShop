import logging
import time

from rabbitmq.common import UsersUpdatesRabbit
from rabbitmq.config import settings


log = logging.getLogger(__name__)


class Producer(UsersUpdatesRabbit):

    def produce_message(self, message):
        message_body = message
        log.info("Send message %s", message_body)
        self.channel.basic_publish(
            exchange=settings.rabbitmq.exchange_name,
            routing_key="",
            body=message_body,
        )
        log.warning("Published message %s", message_body)


def produce(message):
    settings.configure_logging(level=logging.WARNING)
    with Producer() as producer:
        producer.declare_users_updates_exchange()
        producer.produce_message(message=message)
