import asyncio
import csv
from pathlib import Path

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from loguru import logger

from src.enums import QueuesNames
from src.schemas import MetricLogMessage, ModelResponseMessage
from src.settings import settings

metric_log_path = Path("logs/metric_log.csv")
filed_names = ['id', 'y_true','y_pred','absolute_error']
max_digits = 4

broker = RabbitBroker(str(settings.rabbit_mq_dsn))
app = FastStream(broker)


@broker.subscriber(QueuesNames.predictions_queue)
async def handle(msg: ModelResponseMessage) -> MetricLogMessage:
    logger.info(f"Received message: {msg}")

    abs_error = abs(msg.prediction - msg.teacher)
    with open(metric_log_path, mode='a', newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=filed_names)
        log_row = MetricLogMessage(
            id=msg.id,
            y_true=msg.teacher,
            y_pred=round(msg.prediction, max_digits),
            absolute_error=round(abs_error, max_digits)
        )
        writer.writerow(log_row.model_dump())

        logger.info(f"Logged message: {log_row}")

    return log_row


if __name__ == "__main__":
    if not metric_log_path.exists():
        raise FileNotFoundError(f"File {metric_log_path} not found")

    logger.add("logs/evaluation.log", rotation="1 week")
    logger.info("Starting evaluation consumer...")
    asyncio.run(app.run())
