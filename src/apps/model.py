import asyncio
import pickle

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from loguru import logger

from src.enums import QueuesNames
from src.schemas import FeaturesMessage, ModelResponseMessage
from src.settings import settings

broker = RabbitBroker(str(settings.rabbit_mq_dsn))
app = FastStream(broker)

# Читаем файл с сериализованной моделью
with open('src/models/model.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)


@broker.subscriber(QueuesNames.features_queue)
@broker.publisher(QueuesNames.predictions_queue)
async def handle(msg: FeaturesMessage) -> ModelResponseMessage:
    # Предсказываем значение
    prediction = regressor.predict([msg.features])[0]
    logger.info(f"Received message: {msg}, predicted: {prediction}")

    # Отправляем предсказание в очередь
    predict_mess = ModelResponseMessage(
        id_source=msg.id,
        teacher=msg.teacher,
        prediction=prediction,
        created_at=msg.created_at
    )
    logger.info(f"Published message: {predict_mess}")
    return predict_mess


if __name__ == "__main__":
    logger.add("logs/predictions.log", rotation="1 week")
    logger.info("Starting predictions consumer...")
    asyncio.run(app.run())
