import socket
import time
import random
import threading
import webbrowser
class Twitch:
    sock: socket = None
    channel: str = "byte1223"
    # Connect to the IRC server utilizing socket connection. 
    clientToken: str = 'bm5jz15swcewiz2igffjr24h7ijkdl'
    def twitch_connect(self, channel: str) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to Twitch...")
        # Specified twitch socket info.
        self.sock.connect(('irc.chat.twitch.tv', 6667))
        # Connect anonymously.
        user : str = 'justinfan%i' % random.range(100,99999)
        self.sock.send(('NICK %s\r\nPASS fakefan\r\n' % user).encode())
    def reconnect(self, delay: float) -> None:
        time.sleep(delay)
        self.reconnect()
        
## TEST CODE BELOW.
twi = Twitch()
twi.twitch_connect('byte1223')
