from connection.manager import ConnectionManager

manager = ConnectionManager("165.232.46.161", 3010)

while True:
    message = manager.receive_chat_message()
    if message is not None:
        print(message)
