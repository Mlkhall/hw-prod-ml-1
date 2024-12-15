import asyncio

import numpy as np
from faststream.rabbit import RabbitBroker
from loguru import logger
from sklearn.datasets import load_diabetes

from src.constants import RANDOM_SEED, TIME_INTERVAL
from src.enums import QueuesNames
from src.schemas import FeaturesMessage
from src.settings import settings


async def main():
    np.random.seed(RANDOM_SEED)
    train_set, target_set = load_diabetes(return_X_y=True)
    async with RabbitBroker(str(settings.rabbit_mq_dsn)) as broker:
        while True:

            random_row = np.random.randint(0, train_set.shape[0] - 1)
            features_message = FeaturesMessage(
                teacher=target_set[random_row],
                features=train_set[random_row].tolist(),
            )

            await broker.publish(
                message=features_message,
                queue=QueuesNames.features_queue,
            )
            logger.info(f"Published message: {features_message}")

            await asyncio.sleep(TIME_INTERVAL)


if __name__ == "__main__":
    logger.add("logs/features.log", rotation="1 week")
    logger.info("Starting features producer...")
    asyncio.run(main())
