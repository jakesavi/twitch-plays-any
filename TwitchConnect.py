import socket
import time
import random
import threading
import re
import webbrowser


class Twitch:
    SOCK: socket.socket
    CHANNEL: str = "byte1223"
    RE : str = "(?<=\\:)(.*?)(?=\\:)" #Regular Ex. To capture command between two colons Ridding the chat. Focusing only on API response.
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
        user : str = 'justinfan%i' % random.randrange(1,99999)
        self.SOCK.send(('NICK %s\r\nPASS fakefan\r\n' % user).encode())
        self.reciever.start()
        
        
    #Reconnect to socket if disconnected for some reason.
    def reconnect(self, delay: float = 1.0) -> None:
        time.sleep(delay)
        self.twitch_connect()
        
        
    #After recieving the data, figure out parsing. Now we need to ensure we are readding chat.  
    #self.SOCK.send(("JOIN #%s\r\n" % self.CHANNEL).encode())  
    def recieve_message(self) -> None:
        while True:
            data : bytes = self.SOCK.recv(1024)
            if data:
                currentMessage : str = data.decode()
                print(currentMessage)
                for numbRespone in re.findall(self.RE,currentMessage):
                    if "376" in numbRespone:
                        self.SOCK.send(("JOIN #%s\r\n" % self.CHANNEL).encode())
            else:
                pass        
            

    # Actual execution of the parse calls a queue of the chat. If nothing in queue. pass
    def ParcerAndButtonPresser(self) -> None:
        #TODO
        while True:
            try:
                self.QUEUE
                
            except:
                pass
            
            
    #Function will be repeatidly called. for parsing the string and getting the appropriate key.
    def parseForCommand(self, Line: str) -> None:
        
        foundLine = re.search(Twitch.RE, Line)
        if foundLine:
            print(foundLine.group)



j = Twitch()
j.twitch_connect()

