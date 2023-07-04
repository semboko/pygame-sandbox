from servconnction.menage import ConnectionManager

if __name__ == '__main__':
    menage = ConnectionManager("localhost", 32768)

    while True:
        #menage.send_chat_message(input("message: "))
        message = menage.receive_chat_message()
        if message:
            print(message)
