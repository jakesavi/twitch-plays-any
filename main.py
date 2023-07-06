import json
import socket
import Secret
import threading
from pynput import keyboard
##EXAMPLE CODE TAKEN FROM THIS SCRIPT. THIS SCRIPT WAS USE AS A LAUNCHING POINT TO EXPAND THE SOCKET AVAILABILITY.
##EXAMPLE CODE: 
##Put the file name of the json blob here!
JSON: str = "test.json"
##END OF JSON FILE :)
SERVER: str = "irc.twitch.tv"
PORT: int = 6667
BOT: str = "TwitchPlaysAny"
CHANNEL: str = "byte1223"
OWNER: str = "byte1223"
###OATH CODE GOES HERE###
PASS: str = Secret.PASS()
###END OF OATH###
#Twitch is the connection object to chat. 
#Utilize this in main to connect to chat.
class Twitch:

    def __init__(self) -> None:
        irc:socket = socket.socket()
        irc.connect((SERVER,PORT))
        #irc.send("CAP REQ :twitch.tv/commands\n".encode())
        irc.send(("PASS " + PASS + "\n" +
            "NICK " + BOT + "\n" +
            "JOIN #" + CHANNEL + "\n").encode())
        #Loading the controls.
        f = open(JSON)
        data : dict= json.load(f)
        self.control : dict = data.get("Controls")
        print(self.control.get(list(self.control.keys())[0]))
        self.irc: socket = irc



    def sendMessage(self, message: str) -> None: 
        messageTemp :str = "PRIVMSG #" + CHANNEL + " :" + message +"\n"
        #Encode as bytes and ship off the message
        self.irc.send(messageTemp.encode())


    def loadCompleate(self,line:str) -> bool:
        if ("End of /NAMES list" in line):
            print("TwitchBot has jointed " + CHANNEL + "'s Channel!")
            self.sendMessage("Hello World")
            return False
        else:
            return True
        

    def connectToChat(self) -> None:
        Loading :bool = True
        while Loading:
            readbuffer_join:bytes = self.irc.recv(1024)
            readbuffer_join:str = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                Loading :bool = self.loadCompleate(line)
        #When done... Latch to chat and read chat messages!


    def reciever(self) -> None:
        while True:
            bufferRecieved:bytes = self.irc.recv(1024)
            bufferRecieved:str = bufferRecieved.decode()
            for line in bufferRecieved.split("\n")[0:-1]:
                print(line)
                #Prevent premature connection termination
                if "PING :tmi.twitch.tv" in line:
                    self.irc.send("PONG :tmi.twitch.tv".encode())
                    print("PONG :tmi.twitch.tv") 
                if ("PRIVMSG" and "$" in line):
                    #Send Line to Handler Ensure that another thread runs this...
                    command: str = line.split('$')[1]
                    command: str = command.strip("\n")
                    
                    newThread = threading.Thread(target=self.Handler, args=[command]) 
                    newThread.run()

#TODO Fix the fucking handler. This is killing me... :(
    def Handler(self, msg:str):
        #Handler Needs to check the Json blob of data and ensure that it exists in the dictionary
        #Had a weird bug here. Couldn't use in on this json blob?????
        found=False
        for key, val in self.control.items():
            if key == msg:
                found=True
                print("I FOUND THE VALUE")
            else:
                continue

def main():
    t: Twitch = Twitch()
    #Start by connecting to chat.
    t.connectToChat()
    #Then run the reciever.
    t.reciever()
    


    


main()