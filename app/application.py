from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker
from pydantic import BaseModel, Field

class Name(BaseModel):
    name: str = Field(..., description="Name of the person")


class Greeting(BaseModel):
    greeting: str = Field(..., description="Greeting message")


broker = KafkaBroker("localhost:9092")
app = FastStream(broker, title="My service", version="0.1.0", description="My service description")

to_greetings = broker.publisher("greetings")


@broker.subscriber("names")  # type: ignore
async def on_names(msg: Name, logger: Logger) -> None:
    result = f"hello {msg.name}"
    greeting = Greeting(greeting=result)
    await to_greetings.publish(greeting)
