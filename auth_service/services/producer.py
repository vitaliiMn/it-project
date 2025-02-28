import asyncio
from aiokafka import AIOKafkaProducer
import json
import time

class AsyncKafkaProducer:
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def start(self):
        time.sleep(10)
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def send_message(self, username: str):
        message = json.dumps({"username": username}).encode('utf-8')
        await self.producer.send_and_wait(self.topic, message)
    
    async def stop(self):
        await self.producer.stop()

producer = AsyncKafkaProducer(bootstrap_servers='kafka:9092', topic='new_user')

# Пример использования
async def main():
    await producer.start()
    await producer.send_message("DemagoG")
    await producer.stop()
