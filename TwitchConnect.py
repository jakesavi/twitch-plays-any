import socket
import time
import random
import threading
import re
import webbrowser


class Twitch:
    SOCK: socket.socket
    CHANNEL: str = "byte1223"
    RE : str = "" #Regular Ex. To capture command between two colons Ridding the chat. Focusing only on API response.
    # Connect to the IRC server utilizing socket connection. 
    CTOKEN: str = 'bm5jz15swcewiz2igffjr24h7ijkdl'
    #This queue is used by the executer thread.
    QUEUE : list[str]
    reciever : threading.Thread 
    executer: threading.Thread
    def __init__(self) -> None:
        self.reciever= threading.Thread(target=self.recieve_message)
        
    def twitch_connect(self) -> None:
        self.SOCK  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to Twitch...")
        # Specified twitch socket info.
        self.SOCK.connect(('irc.chat.twitch.tv', 6667))
        # Connect anonymously.
        user : str = 'justinfan%i' % random.randrange(100,99999)
        self.SOCK.send(('NICK %s\r\nPASS fakefan\r\n' % user).encode())
        self.reciever.start()        
        
    def reconnect(self, delay: float) -> None:
        time.sleep(delay)
        self.twitch_connect()
        
        
    #After recieving the data, figure out parsing. Now we need to ensure we are readding chat.    
    def recieve_message(self) -> None:
        while True:
            data : bytes = self.SOCK.recv(1024)
            if data:
                currentMsg : str = data.decode()
                print(data.decode())
                #376 defines a ready state of the API. Time to join a channel!
                if "376" in currentMsg:
                    self.connect_to_channel()
            else:
                break
    # Actual execution of the parse calls a queue of the chat. If nothing in queue. pass
    def execution(self) -> None:
        #TODO
        while True:
            try:
                self.QUEUE
                
            except:
                pass
            
    #Function will be repeatidly called. for parsing the string and getting the appropriate key.
    def parseForCommand(self, Line: str) -> None:
        #TODO
        re.match(Twitch.RE, Line)
        
    def connect_to_channel(self) -> None:
        self.SOCK.send((('JOIN #%s\r\n'% self.CHANNEL)).encode())
        
        
## TEST CODE BELOW.

