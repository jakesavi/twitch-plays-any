import json
import socket
import threading
import PySimpleGUI as sg
##EXAMPLE CODE TAKEN FROM THIS SCRIPT. THIS SCRIPT WAS USE AS A LAUNCHING POINT TO EXPAND THE SOCKET AVAILABILITY.
##EXAMPLE CODE: 

SERVER: str = "irc.twitch.tv"
PORT: int = 6667
BOT: str = "TwitchPlaysAny"
CHANNEL: str = "byte1223"

###OATH CODE GOES HERE###
PASS: str = ""
###END OF OATH###
user: str = ""
message: str = ""
#Twitch is the connection object to chat. 
#Utilize this in main to connect to chat.
class Twitch:

    def __init__(self) -> None:
        irc:socket = socket.socket()
        irc.connect((SERVER,PORT))
        irc.send(("PASS " + PASS + "\n" +
          "NICK " + BOT + "\n" +
          "JOIN #" + CHANNEL + "\n").encode())

        self.irc = irc

    def loadCompleate(self,line:str) -> bool:
        if ("End of /NAMES list" in line):
            print("TwitchBot has jointed " + CHANNEL + "'s Channel!")
            self.sendMessage(self.irc, "Hello World")
            return False
        else:
            return True
        
    def sendMessage(self ,irc: socket, message: str) -> None: 
        messageTemp :str = "PRIVMSG #" + CHANNEL + " :" + message

    def connectToChat(self) -> None:
        Loading :bool = True
        while Loading:
            readbuffer_join:bytes = self.irc.recv(1024)
            readbuffer_join:str = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading = self.loadCompleate(line)
    

def reciever() -> None:
    #TODO? 