from consumer import kafka_consumer
import asyncio

async def main():
    kafka_consumer.create_topic()
    await kafka_consumer.consume()


if __name__ == "__main__":
    asyncio.run(main())