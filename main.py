from chat_client import *
from chat_server import *
import time


def main():
    server = Server()
    server.main()
    client = GuiClient()
    client2 = GuiClient()


if __name__ == "__main__":
    main()
