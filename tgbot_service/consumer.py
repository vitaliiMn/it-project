import json

import time

from aiokafka import AIOKafkaConsumer
from confluent_kafka.admin import AdminClient, NewTopic
from mainBot import bot

class KafkaConsumer:
    
    def __init__(self, servers, topic):
        self.servers = servers
        self.topic = topic

    def create_topic(self):
        admin_client = AdminClient({"bootstrap.servers": self.servers})
        new_topic = NewTopic(topic=self.topic, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])

    async def consume(self):
        time.sleep(10)
        consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.servers,
            auto_offset_reset="earliest"
        )
        try:
            await consumer.start()
            async for message in consumer:
                body = json.loads(message.value.decode("utf-8"))
                bot.send_message(body["username"])
        finally:
            await consumer.stop()
            

kafka_consumer = KafkaConsumer("kafka:9092", "new_user")