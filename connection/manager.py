import time
from typing import Optional
import pickle
import pymunk
from redis import Redis
from typing import Dict
from redis.client import PubSub
from scenes.components.player import PlayerMessage, Player


class ConnectionManager:
    def __init__(self, host: str, port: int) -> None:
        self.db = Redis(host, port)
        self.receiver = self.db.pubsub()

        self.receiver.subscribe("chat", "player")

        self.send_delay_sec = 0.1
        self.next_update = time.time() + self.send_delay_sec

        self.receivers: Dict[str, PubSub] = {}

    def add_receiver(self, channel_name: str) -> None:
        new_receiver = self.db.pubsub()
        new_receiver.subscribe(channel_name)
        self.receivers[channel_name] = new_receiver

    def send_chat_message(self, message: str) -> None:
        self.db.publish("chat", message)

    def receive_chat_message(self) -> Optional[str]:
        message = self.receiver.get_message()
        if message is None:
            return
        if message.get("type") == "message":
            return message["data"].decode("UTF-8")

    def receive_player_message(self) -> Optional[PlayerMessage]:
        message = self.receiver.get_message(ignore_subscribe_messages=True)
        if message is not None and message["channel"] == b"player":
            loaded_message = pickle.loads(message.get("data"))
            return loaded_message
        return None

    def send_player_message(self, player: Player) -> None:
        if time.time() < self.next_update:
            return

        pos = player.body.position
        rounded_pos = pymunk.Vec2d(round(pos.x), round(pos.y))
        message = PlayerMessage(
            player_id=player.id,
            player_pos=rounded_pos,
            player_state=player.state,
            player_direction=player.direction,
            player_username=player.username,
        )

        dumped_message = pickle.dumps(message)
        self.db.publish("player", dumped_message)
        self.next_update = time.time() + self.send_delay_sec

