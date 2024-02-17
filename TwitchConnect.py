import socket
import time

class Twitch:
    sock: socket = None
    # Connect to the IRC server utilizing socket connection. 
    def twitch_connect(self, channel: str) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print("Connecting to Twitch...")
        # Specified twitch socket info.
        self.sock.connect(('irc.chat.twitch.tv', 6667))
        # Verify User Utilizing OAUTH or connect anonymously
        

twi = Twitch()        
twi.twitch_connect('byte1223')
