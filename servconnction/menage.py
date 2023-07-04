from typing import Optional

from redis import Redis


class ConnectionManager:

    def __init__(self, host: str, port: int):
        self.db = Redis(host, port)
        self.receiver = self.db.pubsub()

        self.receiver.subscribe("chat")

    def send_chat_message(self, message: str) -> None:
        self.db.publish("chat", message)
    def receive_chat_message(self) -> Optional[str]:
        message = self.receiver.get_message()
        if message is None:
            return
        if message.get("type") == "message":
            return message["data"].decode('utf-8')

        return message
