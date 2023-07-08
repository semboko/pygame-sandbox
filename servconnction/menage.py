from typing import Optional
import pickle
from scenes.components.player import PlayerMessage, Player

from redis import Redis


class ConnectionManager:

    def __init__(self, host: str, port: int):
        self.db = Redis(host, port)
        self.receiver = self.db.pubsub()

        self.receiver.subscribe("chat", "player")

    # def send_chat_message(self, message: str) -> None:
    #     self.db.publish("chat", message)
    #
    # def receive_chat_message(self) -> Optional[str]:
    #     message = self.receiver.get_message()
    #     if message is None:
    #         return
    #     if message.get("type") == "message":
    #         return message["data"].decode('utf-8')
    #
    #     return message

    def receive_player_message(self) -> Optional[PlayerMessage]:
        message = self.receiver.get_message(ignore_subscribe_messages=True)
        if message is None:
            return
        if message["channel"] == b'player':
            return pickle.loads(message.get("data"))
        return

    def send_player_message(self, player: Player) -> None:
        message = PlayerMessage(
            player_id=player.id,
            player_pos=player.body.position,
            player_state=player.state,
            player_direction=player.direction
        )

        dumped_message = pickle.dumps(message)
        self.db.publish("player", dumped_message)

