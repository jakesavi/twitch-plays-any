from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText  
import threading
import json
from pynput import keyboard, mouse
#Creating a new Object for keyboard capture. Naming it as such
class KeyboardCapture:
    queueKey: list[keyboard.Key] = []
    #Key is a weird type that is included in keyboard. 
    def start(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=None) as self.listener:
            self.listener.join()


    def end(self):
        #Terminate existing listener
        self.listener.stop()


    def on_press(self, key: keyboard.Key):
        #Input key to key queue, pass off to other thread. Kinda non-blocking blocking??
        if key == keyboard.Key.esc:
            self.end() #If esc is pressed assume a kill listener request.
            print(self.queueKey)
        else:
            self.queueKey.append(key)
            self.end()




class App:
    MadeJson : dict = {}
    KeyboardListener : KeyboardCapture = KeyboardCapture()
    main :Tk
    def __init__(self) -> None:
        #Threads manage multiple windows. Can't put more than one frame on a thread.

        self.t1: threading.Thread = threading.Thread(target=self.FormNewJsonWindow)
        self.t2: threading.Thread = threading.Thread(target=self.addButton)
        #End of window threads
        self.main = Tk(className="Twitch Plays Any") #Run Main HERE So we can access the main thread elsewhere throughout the object
        self.WindowLaunch()
        self.showJson: Text #Defined in "WindowLaunch"
        
     
    def FormNewJsonWindow(self) -> None:
        newJsonInfo = Tk(className="New Json")
        popUp= ttk.Frame(newJsonInfo, padding=25)
        popUp.grid()
        ttk.Label(popUp, text="Title").grid(row=0)
        ttk.Label(popUp, text="Description").grid(row=1)
        title : ttk.Entry = ttk.Entry(popUp)
        title.grid(row=0,column=0)
        description: ttk.Entry = ttk.Entry(popUp)
        description.grid(row=1,column=0)
        DoneButton: ttk.Button = ttk.Button(popUp, text="Done",command=lambda: self.CloseAndSaveJSON(title.get(), description.get(),window=newJsonInfo))
        DoneButton.grid(row=2,column=1)
        popUp.mainloop() 
        

    def FormNewJson(self):
        self.t1.run()
    def addKey(self):
        self.t2.run()
    def CloseAndSaveJSON(self, title:str, description:str, window:Tk):
        self.MadeJson={"Title": title, "Description": description, "Controls": {}}
        window.destroy()
        print(self.MadeJson)
        #Write Made Json to a file.
        with open(f"{self.MadeJson['Title']}.json", "w") as f:
            f.write(json.dumps(self.MadeJson))
            f.close()
        #Now Write to ShowJson
        self.showJson.config(state=NORMAL)
        self.showJson.delete("1.0",END)
        self.showJson.insert("1.0",json.dumps(self.MadeJson))
        self.showJson.config(state=DISABLED)


    def WindowLaunch(self) -> None: 
        about: str = """Welcome to Twitch plays any!
        How to use: Form a JSON utilizing the key-capture tool below. You can also Import and Export your own. Once you make a new JSON it will appear in the text field below.
        NOTE: The text field below is not editable. If you wish to edit the JSON directly simply open it in notepad."""
        frm= ttk.Frame(self.main,name="twitch plays anything")
        frm.grid()
        ttk.Label(frm, text=about).grid(column=0,row=0, columnspan=20, pady=2)
        self.showJson:Text = Text(frm)
        self.showJson.grid(column=0,row=1,columnspan=20,pady=2)
        self.showJson.insert("1.0",json.dumps(self.MadeJson))
        self.showJson.config(state=DISABLED)
        #print(json.dumps(self.MadeJson))
        ttk.Button(frm, text="New JSON", command=self.FormNewJson ).grid(column=9, row=2,sticky=W)
        ttk.Button(frm, text="Add Button", command=self.addKey).grid(column=10,row=2,sticky=W)
        ttk.Button(frm, text="Quit", command=self.main.destroy).grid(column=11,row=2,sticky=W)
        self.main.mainloop()

    def addButton(self):
        #So a noticably a dictionary must contain at least one element before it
        #Returns true. yes its dumb. But its shorter and cleaner.
        if self.MadeJson:
            buttonInsertInfo = Tk(className="listening...")
            button:ttk.Frame = ttk.Frame(buttonInsertInfo, name="listening...",padding=5)
            button.grid()
            ttk.Label(button, text="Listening... Press esc to cancel, press any key to bind a key.").grid()
            self.KeyboardListener.start()
            #Please remember the listner dies after every check. Also its technically blocking...
            if len(KeyboardCapture.queueKey) == 0:
                return
            else:
                newKey: keyboard.Key = self.KeyboardListener.queueKey.pop()
                button.destroy()
                newbutton: ttk.Frame = ttk.Frame(buttonInsertInfo, name="new button")
                newbutton.grid()
                ttk.Label(newbutton, text=f"New Key: {newKey}\n what should twitch chat type to activate this key?").grid(column=0,row=0,columnspan=2)
                ttk.Label(newbutton, text= "What chat types(Case Sensitive):").grid(column=0,row=1) 
                chatEntry:ttk.Entry = ttk.Entry(newbutton)
                chatEntry.grid(column=1,row=1,columnspan=1)
                #Add save and close button here!
        else:
            buttonInsertInfo = Tk(className="err")
            err:ttk.Frame = ttk.Frame(buttonInsertInfo, name="error", padding=5)
            err.grid()
            ttk.Label(err, text="Please click form a New Json before adding key binds.").grid(column=0,row=0)
            buttonInsertInfo.mainloop()




def Main():
    instance:App = App()
    


Main()