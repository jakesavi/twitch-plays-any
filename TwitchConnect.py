import socket
import time
import random
import threading
from TwitchPlays_KeyCodes import *


class Twitch:
    SOCK: socket.socket
    CHANNEL: str = "demolitiondaisy"
    # Connect to the IRC server utilizing socket connection. 
    CTOKEN: str = 'bm5jz15swcewiz2igffjr24h7ijkdl'
    #This queue is used by the executer thread.
    QUEUE : list[str]
    reciever : threading.Thread 
   #keepMeAliveThread: threading.Thread
    user: str = ""
    ControllerLayout  = {"GameTitle" : "Pokemon Emerald",
                         "Controls" : {'!left':J,
                                       '!down':K,
                                       '!right':L,
                                       '!up':I,
                                       '!b':Z,
                                       '!a':X,
                                       '!select':BACKSPACE,
                                       '!start':ENTER}}
    def __init__(self) -> None:
        self.reciever= threading.Thread(target=self.recieve_message)
    def twitch_connect(self) -> None:
        self.SOCK  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to Twitch...")
        # Specified twitch socket info.
        self.SOCK.connect(('irc.chat.twitch.tv', 6667))
        # Connect anonymously.
        self.user : str = 'justinfan%i' % random.randrange(1,99999)
        self.SOCK.send(('NICK %s\r\nPASS fakefan\r\n' % self.user).encode())
        self.recieve_message()
    #Reconnect to socket if disconnected for some reason.
        # Connect anonymously.
    def recieve_message(self)->None:
        while True:
            try:
                lines = self.BlockToList(self.SOCK.recv(4096).decode())
            except Exception as e:
                print("Something went fuckky wukki Disconnecting and reconnecting!")
                self.SOCK.close()
                self.twitch_connect()
            for line in lines:
                line=line.strip()
                LineParsed: list[str] = (line.split(' :'))
                #Sanitization below!
                if len(LineParsed) > 2:
                    LineParsed = [LineParsed[0],''.join(LineParsed[1:])]
                #Print line here!
                print(LineParsed)
                if 'PING' in LineParsed[0]:
                    self.SOCK.send(('PONG :tmi.twitch.tv\r\n').encode())
                if len(LineParsed) != 2:
                    LineParsed.append(' ')
                if '376' in LineParsed[0]:
                    self.SOCK.send(("JOIN #%s\r\n" % self.CHANNEL).encode())
                if 'PRIVMSG' in LineParsed[0] and LineParsed[1][0] == '!':
                    self.ButtonPresser(LineParsed[1])
                
                


    #After recieving the data, figure out parsing. Now we need to ensure we are readding chat.  
    #self.SOCK.send(("JOIN #%s\r\n" % self.CHANNEL).encode())  
    def BlockToList(self,Block) -> list[str]:
        listContainer : list[str] = Block.split("\r\n")
        return listContainer
            

    # Actual execution of the parse calls a queue of the chat. If nothing in queue. pass
    def ButtonPresser(self, msg: str):
        CommandDictionary : dict[str,str] = self.ControllerLayout.get("Controls")
        if msg.lower() in CommandDictionary:
            HoldAndReleaseKey(CommandDictionary[msg], .1)
            

        
            
    
        
        



j = Twitch()
j.twitch_connect()

